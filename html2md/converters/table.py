"""HTML表格元素转换器。

本模块提供将HTML表格转换为Markdown表格的功能。
"""

from typing import List
from bs4 import Tag


class TableConverter:
    """HTML表格元素到Markdown的转换器。
    
    本类处理table、thead、tbody、tr、th和td标签到Markdown表格格式的转换。
    
    示例:
        converter = TableConverter()
        md = converter.convert(table_tag)
    """
    
    def __init__(self) -> None:
        """初始化表格转换器。"""
        self.supported_tags = {'table', 'thead', 'tbody', 'tr', 'th', 'td'}
    
    def convert(self, tag: Tag) -> str:
        """将HTML表格转换为Markdown。
        
        Args:
            tag: 要转换的表格标签。
        
        Returns:
            Markdown表格表示。
        """
        if tag.name.lower() == 'table':
            return self._convert_table(tag)
        return ""
    
    def _convert_table(self, table: Tag) -> str:
        """转换完整的表格元素。
        
        Args:
            table: 要转换的表格元素。
        
        Returns:
            Markdown表格字符串。
        """
        rows = table.find_all('tr')
        if not rows:
            return ""
        
        result = []
        header_processed = False
        
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if not cells:
                continue
            
            cell_texts = [self._get_cell_text(cell) for cell in cells]
            result.append('| ' + ' | '.join(cell_texts) + ' |')
            
            if not header_processed and row.find('th'):
                result.append(self._create_separator(len(cells)))
                header_processed = True
        
        return '\n'.join(result) + '\n\n'
    
    def _get_cell_text(self, cell: Tag) -> str:
        """获取表格单元格的文本内容。
        
        Args:
            cell: 表格单元格元素。
        
        Returns:
            单元格的文本内容。
        """
        return cell.get_text().strip()
    
    def _create_separator(self, num_columns: int) -> str:
        """创建表格分隔行。
        
        Args:
            num_columns: 表格的列数。
        
        Returns:
            分隔行字符串。
        """
        return '| ' + ' | '.join(['---' for _ in range(num_columns)]) + ' |'
    
    def can_convert(self, tag_name: str) -> bool:
        """检查此转换器是否可以处理特定标签。
        
        Args:
            tag_name: 要检查的标签名。
        
        Returns:
            如果转换器可以处理该标签则返回True，否则返回False。
        """
        return tag_name.lower() in self.supported_tags
