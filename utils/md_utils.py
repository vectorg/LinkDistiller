import os
import re

def create_markdown_table():
    """创建Markdown表格头部"""
    return """# 文章数据记录

| 序号 | 标题 | 链接 | 原文文件路径 | 总结文件路径 | 文章发布日期 | 添加日期时间 |
|------|------|------|-------------|-------------|-------------|-------------|
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

def append_to_markdown_table(md_file, idx, title, url, article_file_path, summary_file_path, publish_date, add_datetime):
    """向Markdown文件添加一行数据"""
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
    
    row = f"| {idx} | {title_escaped} | {url_link} | {article_link} | {summary_link} | {publish_date} | {add_datetime} |\n"
    
    with open(md_file, 'a', encoding='utf-8') as f:
        f.write(row) 