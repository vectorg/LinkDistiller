import requests
import json
from dotenv import load_dotenv
import os
from utils.cache_decorator import llm_cache

load_dotenv()

class SiliChat:
    def __init__(self):
        self.url = os.getenv("SILI_BASE_URL","")
        self.api_key = os.getenv("SILI_API_KEY","")
    
    @llm_cache(cache_dir="data/cache/llm_responses", use_cache=True, stream_delay=0.01)
    def chat_completion(self, prompt: str, stream_output: bool = True):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": True,
            "max_tokens": 512,
            "stop": None,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {
                "type": "text"
            },
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "description": "<string>",
                        "name": "<string>",
                        "parameters": {},
                        "strict": False
                    }
                }
            ]
        }

        try:
            response = requests.post(self.url, headers=headers, json=payload, stream=True)
            response.raise_for_status()
            
            full_content = ""
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        line = line[6:]
                        if line.strip() == "[DONE]":
                            break
                        try:
                            chunk = json.loads(line)
                            if chunk.get('choices') and chunk['choices'][0].get('delta', {}).get('content'):
                                content = chunk['choices'][0]['delta']['content']
                                if stream_output:
                                    print(content, end='', flush=True)
                                full_content += content
                        except json.JSONDecodeError:
                            continue
            if stream_output:
                print()
            return full_content
        except requests.exceptions.RequestException as e:
            print(f"请求出错: {e}")
            return None

chat = SiliChat()
# 为了保持向后兼容，提供一个简单的函数接口
def chat_completion(message):
    """向后兼容的函数接口"""
    return chat.chat_completion(message, stream_output=True)

if __name__ == "__main__":
    test_message = "你是谁"
    print("开始流式输出")
    
    # # 使用新的类方法
    # chat = SiliChat()
    # answer = chat.chat_completion(test_message)
    # print("流式输出结束，答案是：")
    # print(answer)
    
    # 或者使用向后兼容的函数
    answer = chat_completion(test_message)
    print("流式输出结束，答案是：")
    print(answer)
