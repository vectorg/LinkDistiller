from nt import times
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import process_url, print_status
from utils.md_utils import init_dirs_and_files, read_processed_urls
from utils.text_utils import read_and_filter_urls

def loop_process_new_links(data_dir='data', wait_seconds=5):
    articles_dir, summaries_dir, md_file, urls_file = init_dirs_and_files(data_dir)
    processed_count = 0

    while True:
        processed_urls, max_index = read_processed_urls(md_file)
        new_url_notes = read_and_filter_urls(urls_file, processed_urls)
        if not new_url_notes:
            time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(time_str, "没有新的链接需要处理，等待新内容...")
            time.sleep(wait_seconds)
            continue  # 继续下一轮检测
        print(f"发现 {len(new_url_notes)} 个新链接需要处理")
        for url, note in new_url_notes:
            current_index = max_index + processed_count + 1
            success = process_url(url, current_index, articles_dir, summaries_dir, md_file, tags="", note=note)
            processed_count += 1
            print(f"第{current_index}个链接处理完成，已记录到数据文档")
        print_status(processed_count, md_file, articles_dir, summaries_dir, urls_file, no_new_url=(processed_count==0))

if __name__ == '__main__':
    loop_process_new_links()
