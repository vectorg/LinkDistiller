class ColorPrinter:
    def __init__(self):
        self.buffer = ''
        self.in_think = True

    def print_content(self, content: str) -> None:
        """打印带颜色的内容
        
        Args:
            content: 要打印的内容
        """
        # self.buffer += content
        
        # # 如果缓冲区中有完整的</think>标记
        # if self.in_think and '</think>' in self.buffer:
        #     parts = self.buffer.split('</think>', 1)
        #     if parts[0]:  # 打印</think>前的内容
        #         print(colorize(f"{parts[0]}</think>", "bright_cyan"), end='', flush=True)
        #     if parts[1]:  # 打印</think>后的内容
        #         print(colorize(parts[1], "green"), end='', flush=True)
        #     self.buffer = ''
        #     self.in_think = False
        # # 如果没有</think>标记，根据当前状态打印
        # elif len(self.buffer) >= 10:  # 设置一个合理的缓冲区大小
        #     color = "bright_cyan" if self.in_think else "green"
        #     print(colorize(self.buffer, color), end='', flush=True)
        #     self.buffer = ''
        # 直接用蓝色打印
        print(colorize(content, "bright_blue"), end='', flush=True)

def get_color_printer():
    return ColorPrinter()

def colorize(text: str, color: str) -> str:
    """
    为文本添加颜色
    
    Args:
        text: 要着色的文本
        color: 颜色名称
              普通颜色：'red'-红色, 'green'-绿色, 'yellow'-黄色, 
                      'blue'-蓝色, 'purple'-紫色, 'cyan'-青色
              亮色：'bright_red'-亮红色, 'bright_green'-亮绿色, 
                   'bright_yellow'-亮黄色, 'bright_blue'-亮蓝色,
                   'bright_purple'-亮紫色, 'bright_cyan'-亮青色
    
    Returns:
        带有颜色的字符串
    """
    color_map = {
        # 普通颜色
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'purple': 35,
        'cyan': 36,
        # 亮色
        'bright_red': 91,
        'bright_green': 92,
        'bright_yellow': 93,
        'bright_blue': 94,
        'bright_purple': 95,
        'bright_cyan': 96
    }
    
    if color not in color_map:
        raise ValueError(f"不支持的颜色名称: {color}。支持的颜色有: {', '.join(color_map.keys())}")
        
    return f"\033[{color_map[color]}m{text}\033[0m"

if __name__ == "__main__":
    printer = get_color_printer()
    printer.print_content("hello")
    printer.print_content("world")
    printer.print_content("</think>")
    printer.print_content("hello")

    # 打印不同颜色的文本
    print(colorize("这是红色文本", "red"))
    print(colorize("这是绿色文本", "green"))
    print(colorize("这是青色文本", "bright_cyan"))

