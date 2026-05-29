"""TableConverter的单元测试。

本模块测试HTML表格元素到Markdown的转换。
"""

import pytest
from bs4 import BeautifulSoup
from html2md.converters.table import TableConverter


class TestTableConverter:
    """TableConverter类的测试用例。"""
    
    @pytest.fixture
    def converter(self):
        """创建TableConverter实例用于测试。"""
        return TableConverter()
    
    def test_convert_simple_table(self, converter):
        """测试简单表格的转换。"""
        html = '''
        <table>
            <tr>
                <th>Header 1</th>
                <th>Header 2</th>
            </tr>
            <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
            </tr>
        </table>
        '''
        tag = BeautifulSoup(html, 'lxml').find('table')
        result = converter.convert(tag)
        
        assert '| Header 1 | Header 2 |' in result
        assert '| --- | --- |' in result
        assert '| Cell 1 | Cell 2 |' in result
    
    def test_convert_table_no_header(self, converter):
        """测试无表头行的表格的转换。"""
        html = '''
        <table>
            <tr>
                <td>Cell 1</td>
                <td>Cell 2</td>
            </tr>
            <tr>
                <td>Cell 3</td>
                <td>Cell 4</td>
            </tr>
        </table>
        '''
        tag = BeautifulSoup(html, 'lxml').find('table')
        result = converter.convert(tag)
        
        assert '| Cell 1 | Cell 2 |' in result
        assert '| Cell 3 | Cell 4 |' in result
    
    def test_convert_table_with_thead_tbody(self, converter):
        """测试带thead和tbody的表格的转换。"""
        html = '''
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Age</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Alice</td>
                    <td>30</td>
                </tr>
            </tbody>
        </table>
        '''
        tag = BeautifulSoup(html, 'lxml').find('table')
        result = converter.convert(tag)
        
        assert '| Name | Age |' in result
        assert '| --- | --- |' in result
        assert '| Alice | 30 |' in result
    
    def test_convert_table_multiple_columns(self, converter):
        """测试多列表格的转换。"""
        html = '''
        <table>
            <tr>
                <th>Col 1</th>
                <th>Col 2</th>
                <th>Col 3</th>
                <th>Col 4</th>
            </tr>
            <tr>
                <td>A</td>
                <td>B</td>
                <td>C</td>
                <td>D</td>
            </tr>
        </table>
        '''
        tag = BeautifulSoup(html, 'lxml').find('table')
        result = converter.convert(tag)
        
        assert '| Col 1 | Col 2 | Col 3 | Col 4 |' in result
        assert '| --- | --- | --- | --- |' in result
        assert '| A | B | C | D |' in result
    
    def test_convert_empty_table(self, converter):
        """测试空表格的转换。"""
        html = '<table></table>'
        tag = BeautifulSoup(html, 'lxml').find('table')
        result = converter.convert(tag)
        
        assert result == ""
    
    def test_convert_table_empty_row(self, converter):
        """测试带空行的表格的转换。"""
        html = '''
        <table>
            <tr></tr>
            <tr>
                <td>Data</td>
            </tr>
        </table>
        '''
        tag = BeautifulSoup(html, 'lxml').find('table')
        result = converter.convert(tag)
        
        assert '| Data |' in result
    
    def test_can_convert_table(self, converter):
        """测试can_convert方法对table标签的处理。"""
        assert converter.can_convert('table') is True
        assert converter.can_convert('TABLE') is True
    
    def test_can_convert_table_elements(self, converter):
        """测试can_convert方法对表格元素标签的处理。"""
        assert converter.can_convert('thead') is True
        assert converter.can_convert('tbody') is True
        assert converter.can_convert('tr') is True
        assert converter.can_convert('th') is True
        assert converter.can_convert('td') is True
    
    def test_can_convert_non_table_tag(self, converter):
        """测试can_convert方法对非表格标签的处理。"""
        assert converter.can_convert('div') is False
        assert converter.can_convert('span') is False
        assert converter.can_convert('p') is False
    
    def test_create_separator(self, converter):
        """测试分隔符的创建。"""
        separator = converter._create_separator(3)
        assert separator == '| --- | --- | --- |'
        
        separator = converter._create_separator(5)
        assert separator == '| --- | --- | --- | --- | --- |'
    
    def test_get_cell_text(self, converter):
        """测试从表格单元格获取文本。"""
        html = '<td>Cell Content</td>'
        cell = BeautifulSoup(html, 'lxml').find('td')
        text = converter._get_cell_text(cell)
        
        assert text == 'Cell Content'
    
    def test_get_cell_text_with_whitespace(self, converter):
        """测试从带额外空白的单元格获取文本。"""
        html = '<td>  Content with spaces  </td>'
        cell = BeautifulSoup(html, 'lxml').find('td')
        text = converter._get_cell_text(cell)
        
        assert text == 'Content with spaces'
