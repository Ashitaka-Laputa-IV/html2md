"""HTML代码元素转换器。

本模块提供将HTML代码块转换为Markdown的功能。
"""

from typing import Optional
from bs4 import Tag


class CodeConverter:
    """HTML代码元素到Markdown的转换器。
    
    本类处理pre、code和kbd标签到Markdown代码块和内联代码的转换。
    
    示例:
        converter = CodeConverter()
        md = converter.convert(code_tag)
    """
    
    def __init__(self) -> None:
        """初始化代码转换器。"""
        self.supported_tags = {'pre', 'code', 'kbd'}
    
    def convert(self, tag: Tag) -> str:
        """将HTML代码元素转换为Markdown。
        
        Args:
            tag: 要转换的代码元素。
        
        Returns:
            Markdown代码表示。
        """
        tag_name = tag.name.lower()
        
        if tag_name == 'pre':
            return self._convert_pre(tag)
        elif tag_name == 'code':
            return self._convert_code(tag)
        elif tag_name == 'kbd':
            return self._convert_kbd(tag)
        
        return ""
    
    def _convert_pre(self, pre: Tag) -> str:
        """将pre元素转换为代码块。
        
        Args:
            pre: 要转换的pre元素。
        
        Returns:
            Markdown代码块。
        """
        code_tag = pre.find('code')
        if code_tag:
            language = self._get_language(code_tag)
            text = code_tag.get_text()
        else:
            language = ''
            text = pre.get_text()
        
        fence = "```" if "```" not in text else "~~~~"
        return f"{fence}{language}\n{text}\n{fence}\n\n"
    
    def _convert_inline_code(self, code: Tag) -> str:
        """将code/kbd元素转换为内联代码，处理反引号冲突。

        Args:
            code: 要转换的code或kbd元素。

        Returns:
            Markdown内联代码。
        """
        text = code.get_text()
        num_backticks = max(c for c in (text.count('`'), text.count('``'))) + 1
        if num_backticks == 1:
            return f"`{text}`"
        else:
            backticks = '`' * max(2, num_backticks)
            spacer = ' ' if text.startswith('`') else ''
            return f"{backticks}{spacer}{text}{spacer}{backticks}"

    def _convert_code(self, code: Tag) -> str:
        return self._convert_inline_code(code)

    def _convert_kbd(self, kbd: Tag) -> str:
        return self._convert_inline_code(kbd)
    
    def _get_language(self, code: Tag) -> str:
        """从code元素的类中提取编程语言。
        
        Args:
            code: 要分析的code元素。
        
        Returns:
            编程语言名称或空字符串。
        """
        classes = code.get('class', [])
        for cls in classes:
            if cls.startswith('language-'):
                return cls[9:]
            elif cls.startswith('lang-'):
                return cls[5:]
        return ""
    
    def can_convert(self, tag_name: str) -> bool:
        """检查此转换器是否可以处理特定标签。
        
        Args:
            tag_name: 要检查的标签名。
        
        Returns:
            如果转换器可以处理该标签则返回True，否则返回False。
        """
        return tag_name.lower() in self.supported_tags
