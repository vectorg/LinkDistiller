import os
import re

def create_markdown_table():
    """创建Markdown表格头部"""
    return """# 文章数据记录

| 序号 | 标题 | 链接 | 原文文件路径 | 总结文件路径 | 文章发布日期 | 添加日期时间 | 标签 | 说明 |
|------|------|------|-------------|-------------|-------------|-------------|------|------|
"""

def read_processed_urls(md_file):
    """从现有的Markdown文件中读取已处理的链接和最大序号"""
    processed_urls = set()
    max_index = 0
    
    if os.path.exists(md_file):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 使用正则表达式提取链接
            # 匹配 [链接](url) 格式
            url_pattern = r'\[链接\]\((https?://[^\s\)]+)\)'
            urls = re.findall(url_pattern, content)
            processed_urls = set(urls)
            
            # 提取最大序号
            index_pattern = r'^\| (\d+) \|'
            for line in content.split('\n'):
                match = re.match(index_pattern, line)
                if match:
                    index = int(match.group(1))
                    max_index = max(max_index, index)
                    
        except Exception as e:
            print(f"读取现有数据时出错: {e}")
    
    return processed_urls, max_index

def append_to_markdown_table(md_file, idx, title, url, article_file_path, summary_file_path, publish_date, add_datetime, tags="", note=""):
    """向Markdown文件添加一行数据，增加标签和说明字段"""
    # 将文件路径转换为相对路径，使其可以点击
    article_relative_path = os.path.relpath(article_file_path, os.path.dirname(md_file))
    summary_relative_path = os.path.relpath(summary_file_path, os.path.dirname(md_file))
    
    # 创建可点击的文件路径链接
    article_link = f"[原文]({article_relative_path.replace(os.sep, '/')})"
    summary_link = f"[总结]({summary_relative_path.replace(os.sep, '/')})"
    
    # 转义Markdown表格中的特殊字符
    title_escaped = title.replace('|', '\\|').replace('\n', ' ')
    
    # 链接显示为简洁的"链接"文字
    url_link = f"[链接]({url})"
    
    # 新增标签和说明字段
    row = f"| {idx} | {title_escaped} | {url_link} | {article_link} | {summary_link} | {publish_date} | {add_datetime} | {tags} | {note} |\n"
    
    with open(md_file, 'a', encoding='utf-8') as f:
        f.write(row)

def save_article(article_file_path, title, url, publish_date, add_datetime, content):
    with open(article_file_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"**来源链接：** [{url}]({url})\n\n")
        f.write(f"**发布日期：** {publish_date}\n\n")
        f.write(f"**获取时间：** {add_datetime}\n\n")
        f.write("---\n\n")
        f.write(content)

def save_summary(summary_file_path, title, url, current_index, publish_date, add_datetime, summary):
    with open(summary_file_path, 'w', encoding='utf-8') as f:
        f.write(f"# {title} - 总结\n\n")
        f.write(f"**原文链接：** [{url}]({url})\n\n")
        f.write(f"**原文文件：** [点击查看](../articles/article_{current_index}.md)\n\n")
        f.write(f"**发布日期：** {publish_date}\n\n")
        f.write(f"**总结时间：** {add_datetime}\n\n")
        f.write("---\n\n")
        f.write(summary)

def init_dirs_and_files(data_dir):
    articles_dir = os.path.join(data_dir, 'articles')
    summaries_dir = os.path.join(data_dir, 'summaries')
    md_file = os.path.join(data_dir, 'articles_data.md')
    urls_file = os.path.join(data_dir, 'urls.txt')
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(articles_dir, exist_ok=True)
    os.makedirs(summaries_dir, exist_ok=True)
    if not os.path.exists(md_file):
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(create_markdown_table())
    return articles_dir, summaries_dir, md_file, urls_file
