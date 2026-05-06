# -*- coding: utf-8 -*-
"""
CSDN Blog Scraper - A professional, extensible tool for scraping CSDN blog articles.
This package provides comprehensive functionality for scraping blog article
titles, links, publication dates, and view counts from CSDN blogs.

Usage Example:
    from csdn_scraper import CSDNBlogScraper, Config
    
    config = Config(
        blog_url="https://blog.csdn.net/qq_46987323",
        min_delay=1.5,
        max_delay=3.0
    )
    
    scraper = CSDNBlogScraper(config)
    articles = scraper.scrape_all_articles()
    scraper.save_to_csv(articles, "output.csv")
"""

__version__ = "1.0.0"
__author__ = "CSDN Blog Scraper Team"
__license__ = "MIT"

from .scraper import CSDNBlogScraper
from .config import Config
from .exporters import JSONExporter, CSVExporter, TXTExporter, ExporterFactory
from .utils import setup_logger, sanitize_filename

__all__ = [
    "CSDNBlogScraper",
    "Config",
    "JSONExporter",
    "CSVExporter",
    "TXTExporter",
    "ExporterFactory",
    "setup_logger",
    "sanitize_filename",
]
