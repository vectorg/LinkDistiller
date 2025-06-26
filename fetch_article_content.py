import requests
from bs4 import BeautifulSoup

def fetch_article_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # 获取所有可见文本（去除script/style等标签）
        for tag in soup(['script', 'style', 'noscript']):
            tag.decompose()
        text = soup.get_text(separator='\n', strip=True)
        # 去除多余空行
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return '\n'.join(lines)
    except Exception as e:
        print(f"抓取失败: {url}，原因: {e}")
        return ""

if __name__ == "__main__":
    test_url = input("请输入要测试的文章链接：")
    content = fetch_article_content(test_url)
    print("\n--- 网页正文内容 ---\n")
    print(content)
