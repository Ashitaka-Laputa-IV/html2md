"""BaseConverter的单元测试。

本模块测试基础HTML元素到Markdown的转换。
"""

import pytest
from bs4 import BeautifulSoup
from html2md.converters.base import BaseConverter


class TestBaseConverter:
    """BaseConverter类的测试用例。"""
    
    @pytest.fixture
    def converter(self):
        """创建BaseConverter实例用于测试。"""
        return BaseConverter()
    
    @pytest.fixture
    def soup(self):
        """创建BeautifulSoup实例用于解析HTML。"""
        return BeautifulSoup('', 'lxml')
    
    def test_convert_h1(self, converter, soup):
        """测试h1标签的转换。"""
        html = '<h1>Hello World</h1>'
        tag = BeautifulSoup(html, 'lxml').find('h1')
        result = converter.convert(tag)
        assert result == '# Hello World\n\n'
    
    def test_convert_h2(self, converter, soup):
        """测试h2标签的转换。"""
        html = '<h2>Subtitle</h2>'
        tag = BeautifulSoup(html, 'lxml').find('h2')
        result = converter.convert(tag)
        assert result == '## Subtitle\n\n'
    
    def test_convert_h3(self, converter, soup):
        """测试h3标签的转换。"""
        html = '<h3>Section</h3>'
        tag = BeautifulSoup(html, 'lxml').find('h3')
        result = converter.convert(tag)
        assert result == '### Section\n\n'
    
    def test_convert_h4(self, converter, soup):
        """测试h4标签的转换。"""
        html = '<h4>Subsection</h4>'
        tag = BeautifulSoup(html, 'lxml').find('h4')
        result = converter.convert(tag)
        assert result == '#### Subsection\n\n'
    
    def test_convert_h5(self, converter, soup):
        """测试h5标签的转换。"""
        html = '<h5>Minor Heading</h5>'
        tag = BeautifulSoup(html, 'lxml').find('h5')
        result = converter.convert(tag)
        assert result == '##### Minor Heading\n\n'
    
    def test_convert_h6(self, converter, soup):
        """测试h6标签的转换。"""
        html = '<h6>Smallest Heading</h6>'
        tag = BeautifulSoup(html, 'lxml').find('h6')
        result = converter.convert(tag)
        assert result == '###### Smallest Heading\n\n'
    
    def test_convert_paragraph(self, converter, soup):
        """测试段落标签的转换。"""
        html = '<p>This is a paragraph.</p>'
        tag = BeautifulSoup(html, 'lxml').find('p')
        result = converter.convert(tag)
        assert result == 'This is a paragraph.\n\n'
    
    def test_convert_paragraph_empty(self, converter, soup):
        """测试空段落标签的转换。"""
        html = '<p></p>'
        tag = BeautifulSoup(html, 'lxml').find('p')
        result = converter.convert(tag)
        assert result == ''
    
    def test_convert_strong(self, converter, soup):
        """测试strong标签的转换。"""
        html = '<strong>bold text</strong>'
        tag = BeautifulSoup(html, 'lxml').find('strong')
        result = converter.convert(tag)
        assert result == '**bold text**'
    
    def test_convert_b(self, converter, soup):
        """测试b标签的转换。"""
        html = '<b>bold text</b>'
        tag = BeautifulSoup(html, 'lxml').find('b')
        result = converter.convert(tag)
        assert result == '**bold text**'
    
    def test_convert_em(self, converter, soup):
        """测试em标签的转换。"""
        html = '<em>italic text</em>'
        tag = BeautifulSoup(html, 'lxml').find('em')
        result = converter.convert(tag)
        assert result == '*italic text*'
    
    def test_convert_i(self, converter, soup):
        """测试i标签的转换。"""
        html = '<i>italic text</i>'
        tag = BeautifulSoup(html, 'lxml').find('i')
        result = converter.convert(tag)
        assert result == '*italic text*'
    
    def test_convert_link(self, converter, soup):
        """测试锚点标签的转换。"""
        html = '<a href="https://example.com">Example</a>'
        tag = BeautifulSoup(html, 'lxml').find('a')
        result = converter.convert(tag)
        assert result == '[Example](https://example.com)'
    
    def test_convert_link_with_title(self, converter, soup):
        """测试带title的锚点标签的转换。"""
        html = '<a href="https://example.com" title="Example Site">Example</a>'
        tag = BeautifulSoup(html, 'lxml').find('a')
        result = converter.convert(tag)
        assert result == '[Example](https://example.com "Example Site")'
    
    def test_convert_image(self, converter, soup):
        """测试图片标签的转换。"""
        html = '<img src="image.png" alt="An image">'
        tag = BeautifulSoup(html, 'lxml').find('img')
        result = converter.convert(tag)
        assert result == '![An image](image.png)'
    
    def test_convert_image_with_title(self, converter, soup):
        """测试带title的图片标签的转换。"""
        html = '<img src="image.png" alt="An image" title="Image Title">'
        tag = BeautifulSoup(html, 'lxml').find('img')
        result = converter.convert(tag)
        assert result == '![An image](image.png "Image Title")'
    
    def test_convert_unordered_list(self, converter, soup):
        """测试无序列表的转换。"""
        html = '<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>'
        tag = BeautifulSoup(html, 'lxml').find('ul')
        result = converter.convert(tag)
        expected = '- Item 1\n- Item 2\n- Item 3\n\n'
        assert result == expected
    
    def test_convert_ordered_list(self, converter, soup):
        """测试有序列表的转换。"""
        html = '<ol><li>First</li><li>Second</li><li>Third</li></ol>'
        tag = BeautifulSoup(html, 'lxml').find('ol')
        result = converter.convert(tag)
        expected = '1. First\n2. Second\n3. Third\n\n'
        assert result == expected
    
    def test_convert_line_break(self, converter, soup):
        """测试换行标签的转换。"""
        html = '<br>'
        tag = BeautifulSoup(html, 'lxml').find('br')
        result = converter.convert(tag)
        assert result == '  \n'
    
    def test_convert_horizontal_rule(self, converter, soup):
        """测试水平线标签的转换。"""
        html = '<hr>'
        tag = BeautifulSoup(html, 'lxml').find('hr')
        result = converter.convert(tag)
        assert result == '---\n\n'
    
    def test_convert_blockquote(self, converter, soup):
        """测试引用标签的转换。"""
        html = '<blockquote>This is a quote</blockquote>'
        tag = BeautifulSoup(html, 'lxml').find('blockquote')
        result = converter.convert(tag)
        assert result == '> This is a quote\n\n'
    
    def test_convert_blockquote_multiline(self, converter, soup):
        """测试多行引用的转换。"""
        html = '<blockquote>Line 1\nLine 2</blockquote>'
        tag = BeautifulSoup(html, 'lxml').find('blockquote')
        result = converter.convert(tag)
        assert '> Line 1' in result
        assert '> Line 2' in result
    
    def test_can_convert_existing_tag(self, converter):
        """测试can_convert方法对已存在标签的处理。"""
        assert converter.can_convert('h1') is True
        assert converter.can_convert('p') is True
        assert converter.can_convert('a') is True
    
    def test_can_convert_non_existing_tag(self, converter):
        """测试can_convert方法对不存在标签的处理。"""
        assert converter.can_convert('div') is False
        assert converter.can_convert('span') is False
    
    def test_convert_unknown_tag(self, converter, soup):
        """测试未知标签的转换返回文本内容。"""
        html = '<div>Some text</div>'
        tag = BeautifulSoup(html, 'lxml').find('div')
        result = converter.convert(tag)
        assert result == 'Some text'
