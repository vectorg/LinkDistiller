import os
import inspect
import datetime

def debug_print(*args, level="INFO", **kwargs):
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 获取调用者的信息
    frame = inspect.currentframe().f_back
    filename = os.path.basename(frame.f_code.co_filename)
    function_name = frame.f_code.co_name
    line_number = frame.f_lineno
    
    # 打印格式化后的日志信息
    print(f"{current_time} - {level} - {filename}:{function_name}:{line_number} -", end=' ')
    
    # 打印实际内容
    print(*args, **kwargs)

if __name__ == "__main__":
    # 使用示例
    def test_function():
        debug_print("这是一条测试消息")
        debug_print("这是另一条消息", "带多个参数", level="WARNING")
        debug_print("多行\n测试")

    test_function()
    debug_print("在函数外测试")

