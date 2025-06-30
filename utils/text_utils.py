from datetime import datetime
import os

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

def read_and_filter_urls(urls_file, processed_urls):
    if not os.path.exists(urls_file):
        print(f"错误：找不到 {urls_file} 文件")
        return []
    url_note_pairs = []
    with open(urls_file, 'r', encoding='utf-8') as f:
        for line in f:
            url, note = extract_url_and_note(line)
            if url and url not in processed_urls:
                url_note_pairs.append((url, note))
    return url_note_pairs

def extract_url_and_note(line):
    """
    从一行字符串中精确提取第一个http(s)链接，链接前后内容都作为说明。
    返回 (url, note)。
    """
    import re
    line = line.strip()
    if not line:
        return '', ''
    # 匹配第一个http(s)链接
    match = re.search(r'(https?://\S+)', line)
    if match:
        url = match.group(1)
        # 链接前后的内容都作为说明
        note = (line[:match.start()] + line[match.end():]).strip()
        return url, note
    # 没有链接时，全部当说明
    return '', line
