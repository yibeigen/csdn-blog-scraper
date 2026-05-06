# -*- coding: utf-8 -*-
"""
Example 2: Multiple Export Formats
Shows how to export articles in different formats.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src import CSDNBlogScraper, Config


def main():
    print("=" * 60)
    print("Example 2: Multiple Export Formats")
    print("=" * 60)
    
    config = Config(
        blog_url="https://blog.csdn.net/qq_46987323",
        max_pages=1,
    )
    
    scraper = CSDNBlogScraper(config)
    
    articles = scraper.scrape_all_articles()
    
    if articles:
        print("\n📄 Exporting to multiple formats...")
        
        scraper.save_to_txt(articles, "articles.txt")
        scraper.save_to_csv(articles, "articles.csv")
        scraper.save_to_json(articles, "articles.json")
        
        print(f"\n✅ Successfully exported to 3 formats!")


if __name__ == "__main__":
    main()
