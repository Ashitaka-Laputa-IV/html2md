"""基础HTML元素转换器。

本模块提供常见HTML标签的转换器，如标题、段落、
文本格式、链接、图片和列表。
"""

from typing import Optional, Dict, Any, Callable
from bs4 import Tag, NavigableString


class BaseConverter:
    """基础HTML元素到Markdown的转换器。
    
    本类处理常见HTML标签到Markdown等效格式的转换。
    
    示例:
        converter = BaseConverter()
        md = converter.convert(tag, process_children_func)
    """
    
    def __init__(self) -> None:
        """初始化基础转换器。"""
        self.tag_handlers = {
            'h1': self._convert_heading,
            'h2': self._convert_heading,
            'h3': self._convert_heading,
            'h4': self._convert_heading,
            'h5': self._convert_heading,
            'h6': self._convert_heading,
            'p': self._convert_paragraph,
            'strong': self._convert_strong,
            'b': self._convert_strong,
            'em': self._convert_emphasis,
            'i': self._convert_emphasis,
            'a': self._convert_link,
            'img': self._convert_image,
            'ul': self._convert_unordered_list,
            'ol': self._convert_ordered_list,
            'li': self._convert_list_item,
            'br': self._convert_line_break,
            'hr': self._convert_horizontal_rule,
            'blockquote': self._convert_blockquote,
        }
    
    def convert(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将HTML标签转换为Markdown。
        
        Args:
            tag: 要转换的HTML标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            标签的Markdown表示。
        """
        tag_name = tag.name.lower()
        handler = self.tag_handlers.get(tag_name)
        
        if handler:
            return handler(tag, process_children_func)
        
        if process_children_func:
            return process_children_func(tag)
        return self._get_text_content(tag)
    
    def _convert_heading(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将标题标签（h1-h6）转换为Markdown。
        
        Args:
            tag: 要转换的标题标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown标题。
        """
        level = int(tag.name[1])
        text = self._get_processed_content(tag, process_children_func)
        return f"{'#' * level} {text}\n\n"
    
    def _convert_paragraph(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将段落标签转换为Markdown。
        
        Args:
            tag: 要转换的段落标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown段落。
        """
        text = self._get_processed_content(tag, process_children_func)
        if text:
            return f"{text}\n\n"
        return ""
    
    def _convert_strong(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将strong/bold标签转换为Markdown。
        
        Args:
            tag: 要转换的strong或b标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown粗体文本。
        """
        text = self._get_processed_content(tag, process_children_func)
        return f"**{text}**"
    
    def _convert_emphasis(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将emphasis/italic标签转换为Markdown。
        
        Args:
            tag: 要转换的em或i标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown斜体文本。
        """
        text = self._get_processed_content(tag, process_children_func)
        return f"*{text}*"
    
    def _convert_link(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将锚点标签转换为Markdown。
        
        Args:
            tag: 要转换的锚点标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown链接。
        """
        text = self._get_processed_content(tag, process_children_func)
        href = tag.get('href', '')
        title = tag.get('title', '')
        
        if title:
            return f'[{text}]({href} "{title}")'
        return f"[{text}]({href})"
    
    def _convert_image(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将图片标签转换为Markdown。
        
        Args:
            tag: 要转换的图片标签。
            process_children_func: 处理子元素的回调函数（图片标签不使用）。
        
        Returns:
            Markdown图片。
        """
        alt = tag.get('alt', '')
        src = tag.get('src', '')
        title = tag.get('title', '')
        
        if title:
            return f'![{alt}]({src} "{title}")'
        return f"![{alt}]({src})"
    
    def _convert_unordered_list(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将无序列表标签转换为Markdown。
        
        Args:
            tag: 要转换的ul标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown无序列表。
        """
        items = []
        for li in tag.find_all('li', recursive=False):
            text = self._get_processed_content(li, process_children_func)
            items.append(f"- {text}")
        
        return '\n'.join(items) + '\n\n'
    
    def _convert_ordered_list(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将有序列表标签转换为Markdown。
        
        Args:
            tag: 要转换的ol标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown有序列表。
        """
        items = []
        for index, li in enumerate(tag.find_all('li', recursive=False), 1):
            text = self._get_processed_content(li, process_children_func)
            items.append(f"{index}. {text}")
        
        return '\n'.join(items) + '\n\n'
    
    def _convert_list_item(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将列表项标签转换为Markdown。
        
        Args:
            tag: 要转换的li标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown列表项。
        """
        text = self._get_processed_content(tag, process_children_func)
        return f"- {text}"
    
    def _convert_line_break(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将换行标签转换为Markdown。
        
        Args:
            tag: 要转换的br标签。
            process_children_func: 处理子元素的回调函数（换行标签不使用）。
        
        Returns:
            Markdown换行。
        """
        return "  \n"
    
    def _convert_horizontal_rule(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将水平线标签转换为Markdown。
        
        Args:
            tag: 要转换的hr标签。
            process_children_func: 处理子元素的回调函数（水平线标签不使用）。
        
        Returns:
            Markdown水平线。
        """
        return "---\n\n"
    
    def _convert_blockquote(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """将引用标签转换为Markdown。
        
        Args:
            tag: 要转换的blockquote标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            Markdown引用。
        """
        text = self._get_processed_content(tag, process_children_func)
        lines = text.split('\n')
        quoted_lines = [f"> {line}" for line in lines if line.strip()]
        return '\n'.join(quoted_lines) + '\n\n'
    
    def _get_processed_content(self, tag: Tag, process_children_func: Optional[Callable] = None) -> str:
        """获取标签的处理后内容。
        
        如果提供了处理函数，使用它来处理子元素；
        否则直接获取文本内容。
        
        Args:
            tag: 要处理的标签。
            process_children_func: 处理子元素的回调函数。
        
        Returns:
            处理后的内容。
        """
        if process_children_func:
            return process_children_func(tag)
        return self._get_text_content(tag)
    
    def _get_text_content(self, tag: Tag) -> str:
        """获取标签的文本内容。
        
        Args:
            tag: 要提取文本的标签。
        
        Returns:
            标签的文本内容。
        """
        return tag.get_text().strip()
    
    def can_convert(self, tag_name: str) -> bool:
        """检查此转换器是否可以处理特定标签。
        
        Args:
            tag_name: 要检查的标签名。
        
        Returns:
            如果转换器可以处理该标签则返回True，否则返回False。
        """
        return tag_name.lower() in self.tag_handlers
