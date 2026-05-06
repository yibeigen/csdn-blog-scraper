# -*- coding: utf-8 -*-
"""
Example 1: Basic Usage
Shows the simplest way to use the CSDNBlogScraper.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import CSDNBlogScraper, Config


def main():
    print("=" * 60)
    print("Example 1: Basic Usage")
    print("=" * 60)
    
    config = Config(
        blog_url="https://blog.csdn.net/qq_46987323",
        min_delay=1.5,
        max_delay=3.0,
        max_pages=2,
    )
    
    scraper = CSDNBlogScraper(config)
    
    articles = scraper.scrape_all_articles()
    
    if articles:
        scraper.save_to_txt(articles)
        print(f"\n✅ Successfully saved {len(articles)} articles!")


if __name__ == "__main__":
    main()
