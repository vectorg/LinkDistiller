import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

def chat_completion(message):
    url = os.getenv("SILI_BASE_URL")
    api_key = os.getenv("SILI_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [
            {
                "role": "user",
                "content": message
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
        response = requests.post(url, headers=headers, json=payload, stream=True)
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
                            print(content, end='', flush=True)
                            full_content += content
                    except json.JSONDecodeError:
                        continue
        print()
        return full_content
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
        return None

if __name__ == "__main__":
    test_message = "你是谁"
    print("开始流式输出")
    answer = chat_completion(test_message)
    print("流式输出结束，答案是：")
    print(answer)
