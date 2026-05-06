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
        
        # 预定义的 User-Agent 列表
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
        ]
        
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
        # 如果配置了 User-Agent 就用配置的，否则随机选择一个
        user_agent = self.config.user_agent or random.choice(self.user_agents)
        
        headers = {
            'User-Agent': user_agent,
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

            # 简单的反爬虫检测，只在内容特别短的时候才重试
            if len(response.text) < 200:
                self.logger.warning(f"⚠️ Response too short ({len(response.text)} chars), retrying...")
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
        
        # 直接找日期和阅读量（简单直接的方式）
        date_tag = item.find('span', class_='date')
        if date_tag:
            article_info['date'] = date_tag.get_text(strip=True)
        
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
