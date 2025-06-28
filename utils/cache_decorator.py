import os
import hashlib
from utils.debug_print import debug_print
from pathlib import Path
from functools import wraps
import time
import json
from datetime import datetime
from utils.print_utils import get_color_printer, colorize  # 添加colorize导入

def llm_cache(cache_dir="data/cache/llm_responses", use_cache=True, stream_delay=0.001, show_prompt=False):
    """LLM响应缓存装饰器
    Args:
        cache_dir: 缓存目录路径
        use_cache: 是否启用缓存
        stream_delay: 启用缓存时，流式输出时每个字符的延迟时间(秒)
        show_prompt: 是否在控制台输出 prompt
    """
    Path(cache_dir).mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(prompt: str) -> str:
        return hashlib.md5(prompt.encode('utf-8')).hexdigest()
    
    def decorator(func):
        @wraps(func)
        def wrapper(self, prompt: str, stream_output: bool = True, *args, **kwargs):
            if not use_cache:
                return func(self, prompt, stream_output, *args, **kwargs)
            
            cache_key = _get_cache_key(prompt)
            cache_file = os.path.join(cache_dir, f"{cache_key}.txt")
            cache_file_abs = os.path.abspath(cache_file)
            if show_prompt:
                print(colorize(prompt, "bright_green"))
            print(colorize(cache_file_abs, "bright_yellow"))

            if os.path.exists(cache_file):
                with open(cache_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    response_parts = content.split('---- response ----')
                    if len(response_parts) < 2 or not response_parts[1].strip():
                        debug_print(f"缓存文件 {cache_file} 中的响应为空，重新请求", level="WARNING")
                        os.remove(cache_file)  # 删除不完整的缓存文件
                    else:
                        debug_print(f"使用上述缓存文件", level="INFO")
                        response = response_parts[1].strip()
                        if stream_output and stream_delay >= 0:
                            printer = get_color_printer()
                            for char in response:
                                printer.print_content(char)
                                # print('===', char)
                                time.sleep(stream_delay)
                            print()
                        return response
            
            # 先保存提示词和时间戳
            initial_content = f"""---- prompt ----
{prompt}

---- timestamp ----
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---- response ----"""

            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(initial_content)
            
            debug_print("缓存文件不存在，开始请求", level="INFO")
            response = func(self, prompt, stream_output, *args, **kwargs)
            
            # 追加响应内容
            with open(cache_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{response}")
            
            return response
        return wrapper
    return decorator
