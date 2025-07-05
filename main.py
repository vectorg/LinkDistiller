import os
import time
from datetime import datetime
from utils.sili_client import chat_completion
from utils.fetch_article_content import fetch_article_content
from utils.text_utils import extract_title_from_content, extract_date_from_content, read_and_filter_urls
from utils.md_utils import read_processed_urls, append_to_markdown_table, init_dirs_and_files, save_article, save_summary

def summarize_text(text):
    try:
        prompt = f"请用中文总结以下内容：\n{text}"
        summary = chat_completion(prompt)
        return summary.strip() if summary else ""
    except Exception as e:
        print(f"总结失败: {e}")
        return ""

def process_url(url, current_index, articles_dir, summaries_dir, md_file, tags="", note=""):
    print(f"处理第{current_index}个链接: {url}")
    print(f"正在请求原文内容...")
    add_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    article_file_path = os.path.join(articles_dir, f'article_{current_index}.md')
    summary_file_path = os.path.join(summaries_dir, f'summary_{current_index}.md')
    content = fetch_article_content(url)
    if not content:
        title = "获取失败"
        summary = "内容获取失败"
        publish_date = "未知"
        append_to_markdown_table(md_file, current_index, title, url, "内容获取失败", "内容获取失败", publish_date, add_datetime, tags, note)
        return False
    print(f"原文已获取，保存路径: {os.path.abspath(article_file_path)}")
    title = extract_title_from_content(content)
    publish_date = extract_date_from_content(content)
    print(f"文章标题：{title}")
    
    # 过滤说明字段：如果说明开头与标题相同，则移除标题部分
    if note and title and note.startswith(title):
        note = note[len(title):].strip()
    print(f"文章说明：{note}")

    save_article(article_file_path, title, url, publish_date, add_datetime, content)
    print(f"正在用AI总结内容...")
    summary = summarize_text(content[:10000])
    save_summary(summary_file_path, title, url, current_index, publish_date, add_datetime, summary)
    print(f"总结已保存，保存路径: {os.path.abspath(summary_file_path)}")
    append_to_markdown_table(md_file, current_index, title, url, article_file_path, summary_file_path, publish_date, add_datetime, tags, note)
    return True

def print_status(processed_count, md_file, articles_dir, summaries_dir, urls_file, no_new_url=False):
    print(f"\n{'='*50}")
    if no_new_url:
        print("没有新的链接需要处理")
        print(f"当前数据文档路径：{os.path.abspath(md_file)}")
    else:
        print(f"处理完成！共处理 {processed_count} 个新链接")
        print(f"数据文档已保存到：{os.path.abspath(md_file)}")
    print(f"原文文件保存在：{os.path.abspath(articles_dir)}")
    print(f"总结文件保存在：{os.path.abspath(summaries_dir)}")
    print(f"继续添加链接请编辑：{os.path.abspath(urls_file)}")
    print(f"{'='*50}")

def main():
    data_dir = 'data'
    articles_dir, summaries_dir, md_file, urls_file = init_dirs_and_files(data_dir)
    processed_urls, max_index = read_processed_urls(md_file)
    print(f"已处理的链接数量: {len(processed_urls)}")
    print(f"当前最大序号: {max_index}")
    new_url_notes = read_and_filter_urls(urls_file, processed_urls)
    print(f"发现 {len(new_url_notes)} 个新链接需要处理")
    processed_count = 0
    for url, note in new_url_notes:
        current_index = max_index + processed_count + 1
        success = process_url(url, current_index, articles_dir, summaries_dir, md_file, tags="", note=note)
        if success or not success:
            processed_count += 1
        print(f"第{current_index}个链接处理完成，已记录到数据文档")
        # time.sleep(2)
    print_status(processed_count, md_file, articles_dir, summaries_dir, urls_file, no_new_url=(processed_count==0))

if __name__ == "__main__":
    main()
