import os
import time
from datetime import datetime
from utils.sili_client import chat_completion
from utils.fetch_article_content import fetch_article_content
from utils.text_utils import extract_title_from_content, extract_date_from_content, summarize_text
from utils.md_utils import create_markdown_table, read_processed_urls, append_to_markdown_table

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
    
    # 读取已处理的链接和最大序号
    processed_urls, max_index = read_processed_urls(md_file)
    print(f"已处理的链接数量: {len(processed_urls)}")
    print(f"当前最大序号: {max_index}")
    
    # 从data文件夹读取urls.txt
    urls_file = os.path.join(data_dir, 'urls.txt')
    if not os.path.exists(urls_file):
        print(f"错误：找不到 {urls_file} 文件")
        return
    
    with open(urls_file, 'r', encoding='utf-8') as f:
        all_urls = [line.strip() for line in f if line.strip()]
    
    # 过滤出新的链接
    new_urls = [url for url in all_urls if url not in processed_urls]
    
    if not new_urls:
        print("没有新的链接需要处理")
        return
    
    print(f"发现 {len(new_urls)} 个新链接需要处理")
    
    processed_count = 0
    for url in new_urls:
        # 序号从最大序号+1开始
        current_index = max_index + processed_count + 1
        
        print(f"处理第{current_index}个链接: {url}")
        
        # 获取当前时间作为添加日期时间
        add_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 定义文件路径
        article_file_path = os.path.join(articles_dir, f'article_{current_index}.md')
        summary_file_path = os.path.join(summaries_dir, f'summary_{current_index}.md')
        
        # 获取文章内容
        content = fetch_article_content(url)
        if not content:
            # 即使没有内容，也记录到Markdown中
            title = "获取失败"
            summary = "内容获取失败"
            publish_date = "未知"
            append_to_markdown_table(md_file, current_index, title, url, "内容获取失败", "内容获取失败", publish_date, add_datetime)
            processed_count += 1
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
            f.write(f"**原文文件：** [点击查看](../articles/article_{current_index}.md)\n\n")
            f.write(f"**发布日期：** {publish_date}\n\n")
            f.write(f"**总结时间：** {add_datetime}\n\n")
            f.write("---\n\n")
            f.write(summary)
        
        # 写入Markdown数据文档，记录文件路径
        append_to_markdown_table(md_file, current_index, title, url, article_file_path, summary_file_path, publish_date, add_datetime)
        
        processed_count += 1
        print(f"第{current_index}个链接处理完成，已记录到数据文档")
        time.sleep(2)  # 防止API请求过快
    
    # 输出保存的文档路径
    print(f"\n{'='*50}")
    print(f"处理完成！共处理 {processed_count} 个新链接")
    print(f"数据文档已保存到：{os.path.abspath(md_file)}")
    print(f"原文文件保存在：{os.path.abspath(articles_dir)}")
    print(f"总结文件保存在：{os.path.abspath(summaries_dir)}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
