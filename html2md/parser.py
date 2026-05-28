"""HTML解析器模块，使用BeautifulSoup。

本模块提供将HTML字符串解析为结构化格式的功能，
以便于转换为Markdown。
"""

from typing import Optional, List, Any
from bs4 import BeautifulSoup, Tag, NavigableString


class HTMLParser:
    """HTML内容解析器，使用BeautifulSoup。
    
    本类提供解析HTML字符串并提取结构化信息的方法，
    用于转换为Markdown。
    
    属性:
        soup: BeautifulSoup对象，用于解析HTML。
    
    示例:
        parser = HTMLParser('<h1>Hello</h1>')
        elements = parser.get_all_elements()
    """
    
    def __init__(self, html_string: str, parser_type: str = 'lxml') -> None:
        """初始化HTML解析器。
        
        Args:
            html_string: 要解析的HTML字符串。
            parser_type: 使用的解析器（默认：'lxml'）。
                        选项：'lxml', 'html.parser', 'html5lib'
        
        Raises:
            ValueError: 如果html_string为空或None。
        """
        if not html_string or not html_string.strip():
            raise ValueError("HTML字符串不能为空或None")
        
        self.soup = BeautifulSoup(html_string, parser_type)
    
    def get_all_elements(self) -> List[Tag]:
        """获取解析文档中的所有HTML元素。
        
        Returns:
            表示所有HTML元素的Tag对象列表。
        """
        return list(self.soup.find_all(True))
    
    def get_element_by_tag(self, tag_name: str) -> Optional[Tag]:
        """获取具有特定标签名的第一个元素。
        
        Args:
            tag_name: 要查找的标签名。
        
        Returns:
            具有给定名称的第一个Tag对象，如果未找到则返回None。
        """
        return self.soup.find(tag_name)
    
    def get_elements_by_tag(self, tag_name: str) -> List[Tag]:
        """获取具有特定标签名的所有元素。
        
        Args:
            tag_name: 要查找的标签名。
        
        Returns:
            具有给定名称的Tag对象列表。
        """
        return list(self.soup.find_all(tag_name))
    
    def get_text_content(self, element: Tag) -> str:
        """获取元素的文本内容。
        
        Args:
            element: 要提取文本的Tag对象。
        
        Returns:
            元素的文本内容，去除首尾空白。
        """
        if isinstance(element, NavigableString):
            return str(element).strip()
        return element.get_text().strip()
    
    def get_element_attributes(self, element: Tag) -> dict:
        """获取元素的所有属性。
        
        Args:
            element: 要获取属性的Tag对象。
        
        Returns:
            元素属性的字典。
        """
        return dict(element.attrs) if element.attrs else {}
    
    def get_children(self, element: Tag) -> List[Any]:
        """获取元素的所有子元素。
        
        Args:
            element: 要获取子元素的Tag对象。
        
        Returns:
            子元素列表（Tag和NavigableString）。
        """
        return list(element.children)
    
    def has_children(self, element: Tag) -> bool:
        """检查元素是否有子元素。
        
        Args:
            element: 要检查的Tag对象。
        
        Returns:
            如果元素有子元素则返回True，否则返回False。
        """
        return len(list(element.children)) > 0
    
    def prettify(self) -> str:
        """获取解析HTML的格式化版本。
        
        Returns:
            HTML的格式化字符串表示。
        """
        return self.soup.prettify()
