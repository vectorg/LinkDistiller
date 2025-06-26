import os
import time
from sili_fun import chat_completion
from fetch_article_content import fetch_article_content

def summarize_text(text):
    try:
        prompt = f"请用中文总结以下内容：\n{text}"
        summary = chat_completion(prompt)
        return summary.strip() if summary else ""
    except Exception as e:
        print(f"总结失败: {e}")
        return ""

def main():
    # 自动创建文件夹
    os.makedirs('articles', exist_ok=True)
    os.makedirs('summaries', exist_ok=True)
    with open('urls.txt', 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    for idx, url in enumerate(urls, 1):
        print(f"处理第{idx}个链接: {url}")
        content = fetch_article_content(url)
        if not content:
            continue
        with open(f'articles/article_{idx}.txt', 'w', encoding='utf-8') as f:
            f.write(content)
        summary = summarize_text(content[:3000])  # 长文本可截断或分段
        with open(f'summaries/summary_{idx}.txt', 'w', encoding='utf-8') as f:
            f.write(summary)
        time.sleep(2)  # 防止API请求过快

if __name__ == "__main__":
    main()