import os
import time
from datetime import datetime
from sili_fun import chat_completion
from fetch_article_content import fetch_article_content

def extract_title_from_content(content):
    """从内容中提取标题"""
    try:
        # 尝试从内容的前几行提取标题
        lines = content.split('\n')
        for line in lines[:10]:  # 检查前10行
            line = line.strip()
            if line and len(line) < 100:  # 标题通常不会太长
                return line
        return "无标题"
    except:
        return "无标题"

def extract_date_from_content(content):
    """从内容中提取发布日期"""
    try:
        # 这里可以添加更复杂的日期提取逻辑
        # 目前返回当前日期作为占位符
        return datetime.now().strftime("%Y-%m-%d")
    except:
        return datetime.now().strftime("%Y-%m-%d")

def summarize_text(text):
    try:
        prompt = f"请用中文总结以下内容：\n{text}"
        summary = chat_completion(prompt)
        return summary.strip() if summary else ""
    except Exception as e:
        print(f"总结失败: {e}")
        return ""

def create_markdown_table():
    """创建Markdown表格头部"""
    return """# 文章数据记录

| 序号 | 标题 | 链接 | 原文文件路径 | 总结文件路径 | 文章发布日期 | 添加日期时间 |
|------|------|------|-------------|-------------|-------------|-------------|
"""

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

def main():
    # 创建data文件夹
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    
    # 在data文件夹内创建子文件夹
    articles_dir = os.path.join(data_dir, 'articles')
    summaries_dir = os.path.join(data_dir, 'summaries')
    os.makedirs(articles_dir, exist_ok=True)
    os.makedirs(summaries_dir, exist_ok=True)
    
    # 创建Markdown文件路径
    md_file = os.path.join(data_dir, 'articles_data.md')
    
    # 如果Markdown文件不存在，创建并写入表头
    if not os.path.exists(md_file):
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(create_markdown_table())
    
    # 从data文件夹读取urls.txt
    urls_file = os.path.join(data_dir, 'urls.txt')
    if not os.path.exists(urls_file):
        print(f"错误：找不到 {urls_file} 文件")
        return
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    processed_count = 0
    for idx, url in enumerate(urls, 1):
        print(f"处理第{idx}/{len(urls)}个链接: {url}")
        
        # 获取当前时间作为添加日期时间
        add_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 定义文件路径
        article_file_path = os.path.join(articles_dir, f'article_{idx}.md')
        summary_file_path = os.path.join(summaries_dir, f'summary_{idx}.md')
        
        # 获取文章内容
        content = fetch_article_content(url)
        if not content:
            # 即使没有内容，也记录到Markdown中
            title = "获取失败"
            summary = "内容获取失败"
            publish_date = "未知"
            append_to_markdown_table(md_file, idx, title, url, "内容获取失败", "内容获取失败", publish_date, add_datetime)
            continue
        
        # 提取标题和发布日期
        title = extract_title_from_content(content)
        publish_date = extract_date_from_content(content)
        
        # 保存原文为Markdown格式
        with open(article_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"**来源链接：** [{url}]({url})\n\n")
            f.write(f"**发布日期：** {publish_date}\n\n")
            f.write(f"**获取时间：** {add_datetime}\n\n")
            f.write("---\n\n")
            f.write(content)
        
        # 生成总结
        summary = summarize_text(content[:10000])  # 长文本可截断或分段
        with open(summary_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title} - 总结\n\n")
            f.write(f"**原文链接：** [{url}]({url})\n\n")
            f.write(f"**原文文件：** [点击查看](../articles/article_{idx}.md)\n\n")
            f.write(f"**发布日期：** {publish_date}\n\n")
            f.write(f"**总结时间：** {add_datetime}\n\n")
            f.write("---\n\n")
            f.write(summary)
        
        # 写入Markdown数据文档，记录文件路径
        append_to_markdown_table(md_file, idx, title, url, article_file_path, summary_file_path, publish_date, add_datetime)
        
        processed_count += 1
        print(f"第{idx}个链接处理完成，已记录到数据文档")
        time.sleep(2)  # 防止API请求过快
    
    # 输出保存的文档路径
    print(f"\n{'='*50}")
    print(f"处理完成！共处理 {processed_count} 个链接")
    print(f"数据文档已保存到：{os.path.abspath(md_file)}")
    print(f"原文文件保存在：{os.path.abspath(articles_dir)}")
    print(f"总结文件保存在：{os.path.abspath(summaries_dir)}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
