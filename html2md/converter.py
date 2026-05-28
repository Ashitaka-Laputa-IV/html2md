"""HTML转Markdown的主转换器模块。

本模块提供协调HTML到Markdown转换过程的主转换器类。
"""

from typing import Optional, List
from bs4 import BeautifulSoup, Tag, NavigableString

from html2md.parser import HTMLParser
from html2md.converters.base import BaseConverter
from html2md.converters.table import TableConverter
from html2md.converters.code import CodeConverter


class HTML2MarkdownConverter:
    """HTML转Markdown的主转换器类。
    
    本类通过使用各种专门的转换器来协调转换过程。
    
    属性:
        base_converter: 基础元素转换器。
        table_converter: 表格元素转换器。
        code_converter: 代码元素转换器。
    
    示例:
        converter = HTML2MarkdownConverter()
        markdown = converter.convert('<h1>Hello</h1>')
    """
    
    def __init__(self) -> None:
        """初始化HTML转Markdown转换器。"""
        self.base_converter = BaseConverter()
        self.table_converter = TableConverter()
        self.code_converter = CodeConverter()
        
        self.block_elements = {
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div', 'section',
            'article', 'header', 'footer', 'main', 'aside', 'nav',
            'ul', 'ol', 'li', 'blockquote', 'pre', 'table', 'hr'
        }
    
    def convert(self, html_string: str) -> str:
        """将HTML字符串转换为Markdown。
        
        Args:
            html_string: 要转换的HTML字符串。
        
        Returns:
            HTML的Markdown表示。
        
        Raises:
            ValueError: 如果html_string为空或None。
        """
        if not html_string or not html_string.strip():
            raise ValueError("HTML字符串不能为空或None")
        
        parser = HTMLParser(html_string)
        soup = parser.soup
        
        result = self._process_children(soup)
        
        return self._clean_output(result)
    
    def _process_element(self, element) -> str:
        """处理单个HTML元素。
        
        Args:
            element: 要处理的HTML元素。
        
        Returns:
            元素的Markdown表示。
        """
        if isinstance(element, NavigableString):
            text = str(element)
            if not text.strip():
                return ''
            return text
        
        if not isinstance(element, Tag):
            return ''
        
        tag_name = element.name.lower()
        
        if self.code_converter.can_convert(tag_name):
            return self.code_converter.convert(element)
        elif self.table_converter.can_convert(tag_name):
            return self.table_converter.convert(element)
        elif self.base_converter.can_convert(tag_name):
            if tag_name in self.block_elements:
                return self._convert_block_element(element)
            else:
                return self._convert_inline_element(element)
        
        return self._process_children(element)
    
    def _convert_block_element(self, element: Tag) -> str:
        """转换块级HTML元素。
        
        Args:
            element: 要转换的块元素。
        
        Returns:
            块元素的Markdown表示。
        """
        tag_name = element.name.lower()
        
        if tag_name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(tag_name[1])
            text = self._process_children(element)
            return f"{'#' * level} {text}\n\n"
        elif tag_name == 'p':
            text = self._process_children(element)
            return f"{text}\n\n" if text else ''
        elif tag_name == 'blockquote':
            text = self._process_children(element)
            lines = text.split('\n')
            quoted_lines = [f"> {line}" for line in lines if line.strip()]
            return '\n'.join(quoted_lines) + '\n\n'
        elif tag_name == 'hr':
            return "---\n\n"
        elif tag_name in ['ul', 'ol']:
            return self._convert_list(element)
        elif tag_name == 'li':
            return self._convert_list_item(element)
        else:
            return self._process_children(element)
    
    def _convert_inline_element(self, element: Tag) -> str:
        """转换内联HTML元素。
        
        Args:
            element: 要转换的内联元素。
        
        Returns:
            内联元素的Markdown表示。
        """
        tag_name = element.name.lower()
        
        if tag_name in ['strong', 'b']:
            text = self._process_children(element)
            return f"**{text}**"
        elif tag_name in ['em', 'i']:
            text = self._process_children(element)
            return f"*{text}*"
        elif tag_name == 'a':
            text = self._process_children(element)
            href = element.get('href', '')
            title = element.get('title', '')
            if title:
                return f'[{text}]({href} "{title}")'
            return f"[{text}]({href})"
        elif tag_name == 'img':
            alt = element.get('alt', '')
            src = element.get('src', '')
            title = element.get('title', '')
            if title:
                return f'![{alt}]({src} "{title}")'
            return f"![{alt}]({src})"
        elif tag_name == 'br':
            return "  \n"
        else:
            return self._process_children(element)
    
    def _convert_list(self, element: Tag) -> str:
        """将HTML列表转换为Markdown。
        
        Args:
            element: 要转换的列表元素。
        
        Returns:
            列表的Markdown表示。
        """
        tag_name = element.name.lower()
        items = element.find_all('li', recursive=False)
        
        result = []
        for index, li in enumerate(items, 1):
            text = self._process_children(li)
            if tag_name == 'ul':
                result.append(f"- {text}")
            else:
                result.append(f"{index}. {text}")
        
        return '\n'.join(result) + '\n\n'
    
    def _convert_list_item(self, element: Tag) -> str:
        """将HTML列表项转换为Markdown。
        
        Args:
            element: 要转换的列表项元素。
        
        Returns:
            列表项的Markdown表示。
        """
        text = self._process_children(element)
        return f"- {text}"
    
    def _process_children(self, element) -> str:
        """处理元素的所有子元素。
        
        Args:
            element: 父元素。
        
        Returns:
            所有子元素的连接Markdown。
        """
        result = []
        for child in element.children:
            text = self._process_element(child)
            if text:
                result.append(text)
        
        return ''.join(result)
    
    def _clean_output(self, text: str) -> str:
        """清理输出文本。
        
        Args:
            text: 要清理的文本。
        
        Returns:
            清理后的文本。
        """
        lines = text.split('\n')
        cleaned_lines = []
        prev_empty = False
        
        for line in lines:
            if line.strip():
                cleaned_lines.append(line)
                prev_empty = False
            elif not prev_empty:
                cleaned_lines.append(line)
                prev_empty = True
        
        return '\n'.join(cleaned_lines).strip()
