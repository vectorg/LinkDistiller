import os
import re
from collections import OrderedDict

def clean_articles_data():
    """清理articles_data.md文件，去除重复记录"""
    md_file = 'data/articles_data.md'
    
    if not os.path.exists(md_file):
        print("文件不存在")
        return
    
    # 读取文件内容
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 分割成行
    lines = content.split('\n')
    
    # 提取表头
    header_lines = []
    data_lines = []
    
    for line in lines:
        if line.startswith('|') and '序号' in line:
            header_lines.append(line)
        elif line.startswith('|') and '---' in line:
            header_lines.append(line)
        elif line.startswith('|') and not line.startswith('| 序号'):
            data_lines.append(line)
        elif not line.startswith('|') and line.strip():
            header_lines.append(line)
    
    # 去重数据行，保留每个链接的最新记录
    unique_records = OrderedDict()
    
    for line in data_lines:
        # 提取链接
        url_match = re.search(r'\[链接\]\((https?://[^\s\)]+)\)', line)
        if url_match:
            url = url_match.group(1)
            # 如果链接已存在，用新记录替换旧记录
            unique_records[url] = line
    
    # 重新生成文件内容
    new_content = '\n'.join(header_lines) + '\n'
    
    # 重新编号并添加去重后的数据
    for idx, (url, line) in enumerate(unique_records.items(), 1):
        # 替换序号
        new_line = re.sub(r'^\| \d+ \|', f'| {idx} |', line)
        new_content += new_line + '\n'
    
    # 写回文件
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"清理完成！原始记录数: {len(data_lines)}, 去重后记录数: {len(unique_records)}")

if __name__ == "__main__":
    clean_articles_data() 