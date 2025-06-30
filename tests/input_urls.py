import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import process_url
from utils.md_utils import init_dirs_and_files, read_processed_urls

def main_loop():
    data_dir = 'data'
    articles_dir, summaries_dir, md_file, urls_file = init_dirs_and_files(data_dir)
    processed_urls, max_index = read_processed_urls(md_file)
    processed_count = 0
    print('请输入要处理的链接，输入空行退出：')
    while True:
        url = input('链接: ').strip()
        if not url:
            break
        current_index = max_index + processed_count + 1
        success = process_url(url, current_index, articles_dir, summaries_dir, md_file)
        processed_count += 1
        print(f'第{current_index}个链接处理完成，已记录到数据文档\n')
    print('输入结束。')

if __name__ == '__main__':
    main_loop() 