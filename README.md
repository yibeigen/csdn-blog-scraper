# CSDN博客爬虫

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.2.0-orange.svg)](https://gitee.com/yibeigen/csdn-blog-scraper)
[![Gitee Stars](https://img.shields.io/badge/dynamic/json?label=Stars&query=stargazers_count&url=https%3A%2F%2Fgitee.com%2Fapi%2Fv5%2Frepos%2Fyibeigen%2Fcsdn-blog-scraper&color=orange)](https://gitee.com/yibeigen/csdn-blog-scraper)

一个专业、可扩展的CSDN博客文章爬取工具，支持多种输出格式，提供可视化界面，适合社区使用。

---

## ✨ 功能特性

### 🖥️ 可视化界面（推荐）
- ✅ **一键式操作** - 简单直观的图形界面
- ✅ **实时日志** - 显示运行进度和状态
- ✅ **进度显示** - 动态显示爬取进度
- ✅ **输出目录管理** - 快速打开输出文件夹
- ✅ **图片放大查看** - 点击图片弹出放大窗口
- ✅ **欢迎弹窗** - 启动时显示欢迎和开发者信息
- ✅ **智能记忆** - "今天不弹出"功能，本地JSON存储

### 📦 核心功能
- 📱 **可配置的博客URL** - 支持任意CSDN用户博客
- 📝 **多种分页结构识别** - 自动适配不同的页面布局
- 📊 **完整信息提取** - 标题、发布日期、阅读量、URL
- 📄 **多格式输出** - 支持JSON、CSV、TXT格式
- ⏱️ **请求频率控制** - 可配置的延迟，避免对服务器造成负担
- 🛡️ **错误处理和重试** - 自动重试机制，提高成功率
- 📋 **完整日志记录** - 详细的运行日志，方便调试
- 🎯 **简单易用的API** - 同时支持命令行和Python编程

---

## 👤 关于作者

### 开发者信息

| 信息 | 内容 |
|------|------|
| **昵称** | 艺杯羹 |
| **QQ** | 3057454077 |
| **公众号** | 艺杯羹 |
| **Gitee** | [yibeigen](https://gitee.com/yibeigen) |

### 联系方式

- **QQ群**：等待你加入
- **公众号**：扫码关注获取更多工具和教程

公众号二维码：  
![公众号二维码](docs/公众号.png)

赞赏码：  
如果觉得工具好用，欢迎扫码支持！  
![赞赏码](docs/赞赏码.png)

---

## 🚀 快速开始

### 方法一：使用可执行文件（最简单）

1. 从 [Gitee Releases](https://gitee.com/yibeigen/csdn-blog-scraper/releases) 下载最新版 `CSDN博客爬虫_v5.exe`
2. 双击运行即可使用，无需安装Python！

### 方法二：运行源码（需要Python）

#### 环境要求
- Python 3.8+
- pip

#### 安装依赖

```bash
git clone https://gitee.com/yibeigen/csdn-blog-scraper.git
cd csdn-blog-scraper
pip install -r requirements.txt
```

#### 运行可视化界面

```bash
python gui.py
```

#### 运行命令行版本

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

#### Python API 使用

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

---

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

---

## 📦 打包自己的可执行文件

### 手动构建

```bash
# 安装PyInstaller
pip install pyinstaller

# 打包成单文件，包含图片资源
pyinstaller --onefile --windowed --name="CSDN博客爬虫" --add-data="src;src" --add-data="docs;docs" gui.py
```

打包完成后，可执行文件位于 `dist/CSDN博客爬虫.exe`。

---

## 📂 项目结构

```
csdn-blog-scraper/
├── src/                    # 源代码目录
│   ├── __init__.py       # 包初始化
│   ├── scraper.py        # 核心爬虫类
│   ├── config.py         # 配置管理
│   ├── exporters.py      # 导出器
│   └── utils.py          # 工具函数
├── examples/              # 示例代码
│   ├── basic_usage.py
│   └── multiple_formats.py
├── tests/                 # 测试文件
├── outputs/               # 输出目录（自动创建）
├── docs/                  # 文档和图片目录
│   ├── 公众号.png        # 公众号二维码
│   └── 赞赏码.png        # 赞赏码
├── gui.py                 # 可视化界面入口
├── main.py                # 命令行入口
├── requirements.txt       # 依赖列表
├── README.md             # 项目说明
└── LICENSE               # MIT许可证
```

---

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
      "views": "阅读量: 1000"
    }
  ]
}
```

### CSV 格式

```csv
index,title,url,date,views
1,文章标题,https://blog.csdn.net/...,2024-05-01,阅读量: 1000
```

---

## 🛠️ 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

更多详情请查看 [CONTRIBUTING.md](docs/CONTRIBUTING.md)。

---

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

## ⚠️ 免责声明

- 本工具仅供学习和研究使用
- 请遵守 CSDN 的使用条款和 robots.txt
- 合理设置请求频率，避免对服务器造成不必要的负担
- 使用者需自行承担使用本工具的一切后果

---

## 📞 支持

如有问题或建议，请提交 [Issue](https://gitee.com/yibeigen/csdn-blog-scraper/issues)。

---

## 🙏 致谢

感谢所有为这个项目做出贡献的人！

---

**享受爬取！** 🎉
