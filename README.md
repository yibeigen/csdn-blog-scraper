# CSDN Blog Scraper

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-orange.svg)](https://github.com/yourusername/csdn-blog-scraper)

一个专业、可扩展的CSDN博客文章爬取工具，支持多种输出格式，适合社区使用。

## ✨ 功能特性

- 📱 **可配置的博客URL** - 支持任意CSDN用户博客
- 📝 **多种分页结构识别** - 自动适配不同的页面布局
- 📊 **完整信息提取** - 标题、发布日期、阅读量、URL
- 📄 **多格式输出** - 支持JSON、CSV、TXT格式
- ⏱️ **请求频率控制** - 可配置的延迟，避免对服务器造成负担
- 🛡️ **错误处理和重试** - 自动重试机制，提高成功率
- 📋 **完整日志记录** - 详细的运行日志，方便调试
- 🎯 **简单易用的API** - 同时支持命令行和Python编程

## 📦 安装

### 环境要求

- Python 3.8+
- pip

### 安装依赖

```bash
git clone https://github.com/yourusername/csdn-blog-scraper.git
cd csdn-blog-scraper
pip install -r requirements.txt
```

## 🚀 快速开始

### 命令行使用

```bash
# 基本用法 - 爬取博客并保存为TXT
python main.py -u "https://blog.csdn.net/qq_46987323"

# 保存为CSV格式
python main.py -u "https://blog.csdn.net/yourname" -f csv

# 保存为JSON格式
python main.py -u "https://blog.csdn.net/yourname" -f json

# 指定最大页数（测试用）
python main.py -u "https://blog.csdn.net/yourname" --max-pages 3

# 自定义延迟时间
python main.py -u "https://blog.csdn.net/yourname" --min-delay 2 --max-delay 4

# 详细模式（显示更多日志）
python main.py -u "https://blog.csdn.net/yourname" -v
```

### Python API 使用

```python
from src import CSDNBlogScraper, Config

# 创建配置
config = Config(
    blog_url="https://blog.csdn.net/qq_46987323",
    min_delay=1.5,
    max_delay=3.0,
)

# 创建爬虫实例
scraper = CSDNBlogScraper(config)

# 爬取所有文章
articles = scraper.scrape_all_articles()

# 保存为不同格式
scraper.save_to_txt(articles, "my_articles.txt")
scraper.save_to_csv(articles, "my_articles.csv")
scraper.save_to_json(articles, "my_articles.json")
```

更多示例请查看 [examples/](examples/) 目录。

## 📖 完整文档

### 命令行选项

| 选项 | 简写 | 描述 | 默认值 |
|------|------|------|--------|
| `--url` | `-u` | 目标CSDN博客URL（必填） | - |
| `--format` | `-f` | 输出格式（json/csv/txt） | txt |
| `--output` | `-o` | 输出文件名 | 自动生成 |
| `--min-delay` | - | 最小请求延迟（秒） | 1.5 |
| `--max-delay` | - | 最大请求延迟（秒） | 3.0 |
| `--max-pages` | - | 最大爬取页数 | 全部 |
| `--timeout` | - | 请求超时（秒） | 30 |
| `--retries` | - | 最大重试次数 | 3 |
| `--verbose` | `-v` | 详细模式 | False |
| `--list-formats` | - | 列出可用格式 | - |
| `--help` | `-h` | 显示帮助信息 | - |

### Config 配置类

```python
config = Config(
    blog_url="https://blog.csdn.net/yourname",
    min_delay=1.5,           # 最小延迟（秒）
    max_delay=3.0,           # 最大延迟（秒）
    request_timeout=30,      # 请求超时（秒）
    max_retries=3,           # 最大重试次数
    max_pages=None,          # 最大页数（None = 全部）
    output_dir="outputs",    # 输出目录
    user_agent=None,         # 自定义User-Agent
    verify_ssl=True,         # 验证SSL证书
)
```

## 📂 项目结构

```
csdn-blog-scraper/
├── src/                  # 源代码目录
│   ├── __init__.py      # 包初始化
│   ├── scraper.py       # 核心爬虫类
│   ├── config.py        # 配置管理
│   ├── exporters.py     # 导出器
│   └── utils.py         # 工具函数
├── examples/            # 示例代码
│   ├── basic_usage.py
│   └── multiple_formats.py
├── tests/               # 测试文件
├── outputs/             # 输出目录（自动创建）
├── docs/                # 文档目录
├── main.py              # 命令行入口
├── requirements.txt     # 依赖列表
└── README.md            # 项目说明
```

## 🎯 输出格式示例

### JSON 格式

```json
{
  "metadata": {
    "exported_at": "2024-05-06T14:30:00",
    "article_count": 77
  },
  "articles": [
    {
      "title": "文章标题",
      "url": "https://blog.csdn.net/...",
      "date": "2024-05-01",
      "views": "1000"
    }
  ]
}
```

### CSV 格式

```csv
index,title,url,date,views
1,文章标题,https://blog.csdn.net/...,2024-05-01,1000
```

## 🛠️ 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

更多详情请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md)。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

- 本工具仅供学习和研究使用
- 请遵守 CSDN 的使用条款和 robots.txt
- 合理设置请求频率，避免对服务器造成不必要的负担
- 使用者需自行承担使用本工具的一切后果

## 📞 支持

如有问题或建议，请提交 [Issue](../../issues)。

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

---

**享受爬取！** 🎉
