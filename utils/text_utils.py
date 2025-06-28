from datetime import datetime
from utils.sili_client import chat_completion

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