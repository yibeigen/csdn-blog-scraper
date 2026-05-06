# 贡献指南

感谢您对 CSDN Blog Scraper 项目的关注！我们欢迎各种形式的贡献。

## 📋 贡献类型

### 🐛 Bug 报告
- 检查是否已存在相关 Issue
- 清晰描述问题，包括复现步骤
- 附上错误日志或截图（如果有）

### ✨ 新功能建议
- 详细描述功能需求
- 解释功能的用途和价值
- 如果可能，提供实现思路

### 💻 代码贡献
- 修复 Bug
- 实现新功能
- 优化性能
- 改进文档
- 添加测试

### 📖 文档贡献
- 修复拼写或语法错误
- 改进说明文档
- 添加使用示例

## 🚀 快速开始

### 1. Fork 并克隆

```bash
# Fork 项目到您的账号
# 克隆您的 Fork
git clone https://github.com/your-username/csdn-blog-scraper.git
cd csdn-blog-scraper

# 创建分支
git checkout -b feature/your-feature-name
```

### 2. 开发环境设置

```bash
# 安装依赖
pip install -r requirements.txt

# 运行测试
cd tests
python test_scraper.py
```

### 3. 编码规范

- 遵循 PEP 8 规范
- 使用有意义的变量名
- 添加必要的注释
- 保持代码简洁和可读

### 4. 提交修改

```bash
# 添加修改
git add .

# 提交（使用有意义的提交信息）
git commit -m "feat: add new export format support"

# 推送
git push origin feature/your-feature-name
```

### 5. 开启 Pull Request

从您的分支开启 Pull Request 到主仓库的 `main` 分支。

## 📝 提交信息规范

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>: <description>

<optional body>
```

**类型 (Type):**
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档修改
- `style`: 代码格式调整
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/辅助工具相关

**示例:**
```
feat: add YAML export support
fix: handle timeout more gracefully
docs: update installation guide
```

## 🧪 测试

在提交 PR 之前，请确保：

1. 您的代码通过了所有现有测试
2. 为新功能添加了相应的测试
3. 手动测试过基本功能

## 📄 许可证

提交代码即表示您同意将贡献纳入 MIT 许可证下。

## 🤝 行为准则

我们希望所有贡献者都能遵循以下原则：

- 尊重他人的观点和贡献
- 接受建设性的批评
- 关注对社区最有利的事情

## ❓ 需要帮助？

如果您有问题或需要帮助，请：

1. 查看 [README](../README.md)
2. 搜索现有 Issue
3. 开启新的 Issue 寻求帮助

---

再次感谢您的贡献！🎉
