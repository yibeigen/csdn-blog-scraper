# -*- coding: utf-8 -*-
"""
测试完整爬取 - 获取全部77篇文章
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src import CSDNBlogScraper, Config, setup_logger
import logging

logger = setup_logger(log_file="outputs/test_full.log", log_level=logging.INFO)

print("=" * 70)
print("CSDN博客爬虫 - 完整测试")
print("=" * 70)

# 配置 - 使用较快的延迟，因为已经测试过
config = Config(
    blog_url="https://blog.csdn.net/qq_46987323",
    min_delay=0.8,
    max_delay=1.5,
    max_pages=None,
    output_dir="outputs"
)

scraper = CSDNBlogScraper(config, logger)

print("\n开始爬取文章...")
articles = scraper.scrape_all_articles()

print(f"\n✅ 爬取完成！共 {len(articles)} 篇文章")

# 保存为多种格式
print("\n保存为TXT格式...")
txt_file = scraper.save_to_txt(articles, "csdn_articles_full.txt")
print(f"保存到: {txt_file}")

print("\n保存为CSV格式...")
csv_file = scraper.save_to_csv(articles, "csdn_articles_full.csv")
print(f"保存到: {csv_file}")

print("\n保存为JSON格式...")
json_file = scraper.save_to_json(articles, "csdn_articles_full.json")
print(f"保存到: {json_file}")

print("\n" + "=" * 70)
print("🎉 全部完成！")
print("=" * 70)
