# -*- coding: utf-8 -*-
"""Debug script to check page structure."""
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = "https://blog.csdn.net/qq_46987323/article/list/1"

ua = UserAgent()
headers = {
    'User-Agent': ua.random,
}

response = requests.get(url, headers=headers, timeout=30)
print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.text, 'lxml')

# 保存HTML到文件查看
with open('debug_output.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

print("\n" + "="*60)
print("Looking for article containers...")
print("="*60)

# 尝试多种选择器
selectors_to_try = [
    ('div.article-item-box', soup.select('div.article-item-box')),
    ('article.blog-list-box', soup.select('article.blog-list-box')),
    ('div.article-list', soup.select('div.article-list')),
    ('div[class*="article"]', soup.select('div[class*="article"]')),
    ('div[data-v-]', soup.select('div[data-v-]')),
    ('div[class*="list"]', soup.select('div[class*="list"]')),
]

for name, elements in selectors_to_try:
    print(f"\n{name}: {len(elements)} elements found")
    if elements and len(elements) > 0:
        print(f"  Example class: {elements[0].get('class', '')}")
        print(f"  First 200 chars: {str(elements[0])[:200]}...")
