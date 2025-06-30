# LinkDistiller - 链接内容提取与总结工具

## 功能说明

这是一个用于提取网页内容并生成总结的工具，所有数据均以 Markdown 格式存储，支持文件路径点击跳转。

## 主要特性

- 🔗 **链接提取**：从 `data/urls.txt` 文件读取链接并提取内容
- 📝 **Markdown格式**：所有文件均以 Markdown 格式存储，便于阅读和编辑
- 🔗 **可点击路径**：在数据表格中的文件路径可直接点击跳转
- 📊 **结构化数据**：使用 Markdown 表格记录所有文章信息
- 📄 **原文保存**：保存完整的原文内容
- 📋 **智能总结**：调用 AI（通过 `utils/sili_client.py`）生成文章总结
- 🕒 **自动记录时间**：自动记录文章发布日期和处理时间
- 🧩 **模块化设计**：核心功能拆分在 `utils/` 目录下，便于维护和扩展
- 🖊️ **交互式输入**：支持通过 `tests/input_urls.py` 脚本交互式输入链接，并即时处理和总结

## 文件结构

```text
data/
├── articles_data.md          # 主数据表格（Markdown格式）
├── urls.txt                  # 待处理的链接列表
├── articles/                 # 原文存储目录
│   ├── article_1.md
│   ├── article_2.md
│   └── ...
└── summaries/                # 总结存储目录
    ├── summary_1.md
    ├── summary_2.md
    └── ...
utils/
├── cache_decorator.py        # 缓存装饰器
├── debug_print.py            # 调试打印工具
├── fetch_article_content.py  # 网页内容抓取
├── md_utils.py               # Markdown 相关工具
├── print_utils.py            # 打印工具
├── sili_client.py            # AI 总结接口
└── text_utils.py             # 文本处理工具
main.py                       # 主程序入口
tests/
└── input_urls.py             # 交互式输入并即时处理链接
```

## 数据表格格式

主数据表格 `articles_data.md` 包含以下列：

| 列名         | 说明           | 格式         |
|--------------|----------------|--------------|
| 序号         | 处理顺序编号   | 数字         |
| 标题         | 文章标题       | 文本         |
| 链接         | 原始URL        | 可点击链接   |
| 原文文件路径 | 原文文件位置   | 可点击链接   |
| 总结文件路径 | 总结文件位置   | 可点击链接   |
| 文章发布日期 | 文章发布日期   | 日期         |
| 添加日期时间 | 处理时间       | 日期时间     |

## 使用方法

### 方式一：批量处理
1. 在 `data/urls.txt` 文件中添加要处理的链接（每行一个）
2. 运行主程序：
   ```bash
   python main.py
   ```
3. 查看生成的 `data/articles_data.md` 文件
4. 点击表格中的文件路径链接可以直接跳转到对应文件

### 方式二：交互式即时处理
1. 运行交互式输入脚本：
   ```bash
   python tests/input_urls.py
   ```
2. 按提示输入链接，每输入一个链接会立即下载内容、生成总结并保存，输入空行退出
3. 处理结果会实时显示，所有数据同样写入 Markdown 文件和目录

## 主要模块说明

- `main.py`：主流程控制，负责调度各功能模块
- `tests/input_urls.py`：交互式输入链接并即时处理
- `utils/fetch_article_content.py`：抓取网页原文内容
- `utils/text_utils.py`：提取标题、发布日期、过滤已处理链接
- `utils/md_utils.py`：Markdown 文件的读写、表格追加、目录初始化等
- `utils/sili_client.py`：AI 总结接口
- 其他 utils 文件为辅助工具

## 文件格式说明

### 原文文件 (articles/article_X.md)
- 包含完整的文章标题、来源链接、发布日期、抓取时间及正文内容
- Markdown 格式，便于阅读和编辑

### 总结文件 (summaries/summary_X.md)
- 包含 AI 生成的文章总结
- 提供原文链接和文件路径的快速跳转
- Markdown 格式

### 数据表格 (articles_data.md)
- Markdown 表格格式
- 所有文件路径均为可点击链接
- 支持在支持 Markdown 的编辑器中直接点击跳转
