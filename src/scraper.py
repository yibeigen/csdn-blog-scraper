# -*- coding: utf-8 -*-
"""
Core scraper class for the CSDN Blog Scraper.
Handles HTTP requests, HTML parsing, and article extraction.
"""

import time
import random
import re
import logging
from typing import List, Dict, Any, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from .config import Config
from .utils import setup_logger, extract_username
from .exporters import ExporterFactory


class CSDNBlogScraper:
    """
    Main scraper class for CSDN blogs.
    
    Features:
        - Scrapes article titles, URLs, publication dates, and view counts
        - Supports multiple page structures
        - Rate limiting with configurable delays
        - Automatic retry on failure
        - Multiple output formats
    """
    
    def __init__(self, config: Optional[Config] = None, logger: Optional[logging.Logger] = None):
        """
        Initialize the scraper.
        
        Args:
            config: Configuration object (uses defaults if None)
            logger: Logger instance (creates new if None)
        """
        self.config = config or Config()
        self.logger = logger or setup_logger(
            log_file=f"{self.config.output_dir}/scraper.log"
        )
        self.session = requests.Session()
        self.ua = UserAgent()
        
        self.username = extract_username(self.config.blog_url)
        self.logger.info(f"📱 Target blog: {self.config.blog_url}")
        self.logger.info(f"👤 Username: {self.username or 'Unknown'}")
        
    def _get_headers(self, referer: Optional[str] = None) -> Dict[str, str]:
        """
        Get HTTP headers for requests.
        
        Args:
            referer: Referer URL (optional)
            
        Returns:
            Dictionary of HTTP headers
        """
        headers = {
            'User-Agent': self.config.user_agent or self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        if referer:
            headers['Referer'] = referer
        
        return headers
    
    def _random_delay(self):
        """Add random delay between requests."""
        delay = random.uniform(self.config.min_delay, self.config.max_delay)
        self.logger.debug(f"⏱️ Waiting {delay:.1f} seconds...")
        time.sleep(delay)
    
    def _safe_request(self, url: str, retry: int = 0, referer: Optional[str] = None) -> Optional[requests.Response]:
        """
        Make a safe HTTP request with retries.
        
        Args:
            url: Target URL
            retry: Current retry count
            referer: Referer URL (optional)
            
        Returns:
            Response object if successful, None otherwise
        """
        if retry >= self.config.max_retries:
            self.logger.error(f"❌ Request failed after {self.config.max_retries} attempts: {url}")
            return None
        
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(referer),
                timeout=self.config.request_timeout,
                verify=self.config.verify_ssl
            )
            response.raise_for_status()
            
            if '验证' in response.text or '验证码' in response.text or len(response.text) < 500:
                self.logger.warning(f"⚠️ Possible anti-bot detection, retrying...")
                self._random_delay()
                return self._safe_request(url, retry + 1, referer)
            
            return response
            
        except requests.RequestException as e:
            self.logger.warning(f"⚠️ Request failed: {str(e)}, retrying...")
            self._random_delay()
            return self._safe_request(url, retry + 1, referer)
    
    def _parse_article_item(self, item: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """
        Parse a single article item from the page.
        
        Args:
            item: BeautifulSoup element
            
        Returns:
            Article dictionary with title, url, date, views
        """
        article_info = {}
        
        # 尝试多种方式获取标题和链接
        title_tag = item.find('h4') or item.find('a', class_='title') or item.find('a')
        if title_tag:
            if title_tag.name == 'a':
                link_tag = title_tag
            else:
                link_tag = title_tag.find('a')
            
            if link_tag:
                article_info['title'] = link_tag.get_text(strip=True)
                article_info['url'] = link_tag.get('href', '')
        
        if 'title' not in article_info or not article_info['title']:
            return None
        
        # 尝试多种方式获取日期和阅读量
        # 新结构：colu_auth_b 包含时间和阅读量
        info_div = item.find('div', class_='colu_auth_b') or item.find('div', class_='info-box')
        if info_div:
            spans = info_div.find_all('span')
            for span in spans:
                span_text = span.get_text(strip=True)
                if '阅读' in span_text:
                    article_info['views'] = span_text
                else:
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', span_text)
                    if date_match:
                        article_info['date'] = date_match.group(1)
                    else:
                        article_info['date'] = span_text
        
        # 如果上面没找到，尝试旧的结构
        if 'date' not in article_info:
            date_tag = item.find('span', class_='date') or item.find('div', class_='info-box')
            if date_tag:
                date_text = date_tag.get_text(strip=True)
                date_match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
                if date_match:
                    article_info['date'] = date_match.group(1)
                else:
                    article_info['date'] = date_text
        
        if 'views' not in article_info:
            read_tag = item.find('span', class_='read-num') or item.find('span', class_='read-count')
            if read_tag:
                article_info['views'] = read_tag.get_text(strip=True)
        
        return article_info
    
    def scrape_page(self, page_num: int) -> List[Dict[str, Any]]:
        """
        Scrape a single page of articles.
        
        Args:
            page_num: Page number
            
        Returns:
            List of article dictionaries from the page
        """
        page_url = f"{self.config.blog_url}/article/list/{page_num}"
        self.logger.info(f"📄 Scraping page {page_num}: {page_url}")
        
        response = self._safe_request(page_url, referer=self.config.blog_url)
        if not response:
            self.logger.error(f"❌ Failed to get page {page_num}")
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        selectors = [
            'ul.colu_author_c > li',
            'div.article-item-box',
            'article.blog-list-box',
            'div.article-list > div',
        ]
        
        article_items = []
        for selector in selectors:
            items = soup.select(selector)
            if items:
                article_items = items
                self.logger.debug(f"📝 Found {len(items)} articles using selector: {selector}")
                break
        
        if not article_items:
            self.logger.warning(f"⚠️ No articles found on page {page_num}")
            return []
        
        articles = []
        for item in article_items:
            article_info = self._parse_article_item(item)
            if article_info:
                articles.append(article_info)
                self.logger.debug(f"✅ Article: {article_info['title'][:50]}...")
        
        return articles
    
    def scrape_all_articles(self) -> List[Dict[str, Any]]:
        """
        Scrape all articles from the blog.
        
        Returns:
            Complete list of article dictionaries
        """
        self.logger.info("🚀 Starting scraping process...")
        
        all_articles = []
        page_num = 1
        
        try:
            while True:
                if self.config.max_pages and page_num > self.config.max_pages:
                    self.logger.info(f"✅ Reached max pages limit ({self.config.max_pages})")
                    break
                
                articles = self.scrape_page(page_num)
                
                if not articles:
                    self.logger.info(f"✅ No more articles found (page {page_num})")
                    break
                
                all_articles.extend(articles)
                self.logger.info(f"📊 Page {page_num}: +{len(articles)} articles, Total: {len(all_articles)}")
                
                self._random_delay()
                page_num += 1
                
                if page_num > 100:
                    self.logger.warning(f"⚠️ Stopping after 100 pages to prevent infinite loop")
                    break
            
        except KeyboardInterrupt:
            self.logger.info("\n⚠️ User interrupted scraping process")
        
        self.logger.info(f"🎉 Scraping complete! Total articles: {len(all_articles)}")
        return all_articles
    
    def save(self, articles: List[Dict[str, Any]], format: str = "txt", filename: Optional[str] = None) -> str:
        """
        Save articles to file in specified format.
        
        Args:
            articles: List of article dictionaries
            format: Output format (json, csv, txt)
            filename: Output filename (optional, auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            from datetime import datetime
            from .utils import sanitize_filename
            
            date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_username = sanitize_filename(self.username or "unknown", max_length=30)
            filename = f"csdn_articles_{safe_username}_{date_str}.{format}"
        
        filepath = f"{self.config.output_dir}/{filename}"
        
        exporter = ExporterFactory.get_exporter(format)
        exporter.export(articles, filepath)
        
        return filepath
    
    def save_to_csv(self, articles: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """Convenience method to save as CSV."""
        return self.save(articles, "csv", filename)
    
    def save_to_json(self, articles: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """Convenience method to save as JSON."""
        return self.save(articles, "json", filename)
    
    def save_to_txt(self, articles: List[Dict[str, Any]], filename: Optional[str] = None) -> str:
        """Convenience method to save as TXT."""
        return self.save(articles, "txt", filename)
