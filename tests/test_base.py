"""Unit tests for BaseConverter.

This module tests the conversion of basic HTML elements to Markdown.
"""

import pytest
from bs4 import BeautifulSoup
from html2md.converters.base import BaseConverter


class TestBaseConverter:
    """Test cases for BaseConverter class."""
    
    @pytest.fixture
    def converter(self):
        """Create a BaseConverter instance for testing."""
        return BaseConverter()
    
    @pytest.fixture
    def soup(self):
        """Create a BeautifulSoup instance for parsing HTML."""
        return BeautifulSoup('', 'lxml')
    
    def test_convert_h1(self, converter, soup):
        """Test conversion of h1 tag."""
        html = '<h1>Hello World</h1>'
        tag = BeautifulSoup(html, 'lxml').find('h1')
        result = converter.convert(tag)
        assert result == '# Hello World\n\n'
    
    def test_convert_h2(self, converter, soup):
        """Test conversion of h2 tag."""
        html = '<h2>Subtitle</h2>'
        tag = BeautifulSoup(html, 'lxml').find('h2')
        result = converter.convert(tag)
        assert result == '## Subtitle\n\n'
    
    def test_convert_h3(self, converter, soup):
        """Test conversion of h3 tag."""
        html = '<h3>Section</h3>'
        tag = BeautifulSoup(html, 'lxml').find('h3')
        result = converter.convert(tag)
        assert result == '### Section\n\n'
    
    def test_convert_h4(self, converter, soup):
        """Test conversion of h4 tag."""
        html = '<h4>Subsection</h4>'
        tag = BeautifulSoup(html, 'lxml').find('h4')
        result = converter.convert(tag)
        assert result == '#### Subsection\n\n'
    
    def test_convert_h5(self, converter, soup):
        """Test conversion of h5 tag."""
        html = '<h5>Minor Heading</h5>'
        tag = BeautifulSoup(html, 'lxml').find('h5')
        result = converter.convert(tag)
        assert result == '##### Minor Heading\n\n'
    
    def test_convert_h6(self, converter, soup):
        """Test conversion of h6 tag."""
        html = '<h6>Smallest Heading</h6>'
        tag = BeautifulSoup(html, 'lxml').find('h6')
        result = converter.convert(tag)
        assert result == '###### Smallest Heading\n\n'
    
    def test_convert_paragraph(self, converter, soup):
        """Test conversion of paragraph tag."""
        html = '<p>This is a paragraph.</p>'
        tag = BeautifulSoup(html, 'lxml').find('p')
        result = converter.convert(tag)
        assert result == 'This is a paragraph.\n\n'
    
    def test_convert_paragraph_empty(self, converter, soup):
        """Test conversion of empty paragraph tag."""
        html = '<p></p>'
        tag = BeautifulSoup(html, 'lxml').find('p')
        result = converter.convert(tag)
        assert result == ''
    
    def test_convert_strong(self, converter, soup):
        """Test conversion of strong tag."""
        html = '<strong>bold text</strong>'
        tag = BeautifulSoup(html, 'lxml').find('strong')
        result = converter.convert(tag)
        assert result == '**bold text**'
    
    def test_convert_b(self, converter, soup):
        """Test conversion of b tag."""
        html = '<b>bold text</b>'
        tag = BeautifulSoup(html, 'lxml').find('b')
        result = converter.convert(tag)
        assert result == '**bold text**'
    
    def test_convert_em(self, converter, soup):
        """Test conversion of em tag."""
        html = '<em>italic text</em>'
        tag = BeautifulSoup(html, 'lxml').find('em')
        result = converter.convert(tag)
        assert result == '*italic text*'
    
    def test_convert_i(self, converter, soup):
        """Test conversion of i tag."""
        html = '<i>italic text</i>'
        tag = BeautifulSoup(html, 'lxml').find('i')
        result = converter.convert(tag)
        assert result == '*italic text*'
    
    def test_convert_link(self, converter, soup):
        """Test conversion of anchor tag."""
        html = '<a href="https://example.com">Example</a>'
        tag = BeautifulSoup(html, 'lxml').find('a')
        result = converter.convert(tag)
        assert result == '[Example](https://example.com)'
    
    def test_convert_link_with_title(self, converter, soup):
        """Test conversion of anchor tag with title."""
        html = '<a href="https://example.com" title="Example Site">Example</a>'
        tag = BeautifulSoup(html, 'lxml').find('a')
        result = converter.convert(tag)
        assert result == '[Example](https://example.com "Example Site")'
    
    def test_convert_image(self, converter, soup):
        """Test conversion of image tag."""
        html = '<img src="image.png" alt="An image">'
        tag = BeautifulSoup(html, 'lxml').find('img')
        result = converter.convert(tag)
        assert result == '![An image](image.png)'
    
    def test_convert_image_with_title(self, converter, soup):
        """Test conversion of image tag with title."""
        html = '<img src="image.png" alt="An image" title="Image Title">'
        tag = BeautifulSoup(html, 'lxml').find('img')
        result = converter.convert(tag)
        assert result == '![An image](image.png "Image Title")'
    
    def test_convert_unordered_list(self, converter, soup):
        """Test conversion of unordered list."""
        html = '<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>'
        tag = BeautifulSoup(html, 'lxml').find('ul')
        result = converter.convert(tag)
        expected = '- Item 1\n- Item 2\n- Item 3\n\n'
        assert result == expected
    
    def test_convert_ordered_list(self, converter, soup):
        """Test conversion of ordered list."""
        html = '<ol><li>First</li><li>Second</li><li>Third</li></ol>'
        tag = BeautifulSoup(html, 'lxml').find('ol')
        result = converter.convert(tag)
        expected = '1. First\n2. Second\n3. Third\n\n'
        assert result == expected
    
    def test_convert_line_break(self, converter, soup):
        """Test conversion of line break tag."""
        html = '<br>'
        tag = BeautifulSoup(html, 'lxml').find('br')
        result = converter.convert(tag)
        assert result == '  \n'
    
    def test_convert_horizontal_rule(self, converter, soup):
        """Test conversion of horizontal rule tag."""
        html = '<hr>'
        tag = BeautifulSoup(html, 'lxml').find('hr')
        result = converter.convert(tag)
        assert result == '---\n\n'
    
    def test_convert_blockquote(self, converter, soup):
        """Test conversion of blockquote tag."""
        html = '<blockquote>This is a quote</blockquote>'
        tag = BeautifulSoup(html, 'lxml').find('blockquote')
        result = converter.convert(tag)
        assert result == '> This is a quote\n\n'
    
    def test_convert_blockquote_multiline(self, converter, soup):
        """Test conversion of multiline blockquote."""
        html = '<blockquote>Line 1\nLine 2</blockquote>'
        tag = BeautifulSoup(html, 'lxml').find('blockquote')
        result = converter.convert(tag)
        assert '> Line 1' in result
        assert '> Line 2' in result
    
    def test_can_convert_existing_tag(self, converter):
        """Test can_convert method with existing tag."""
        assert converter.can_convert('h1') is True
        assert converter.can_convert('p') is True
        assert converter.can_convert('a') is True
    
    def test_can_convert_non_existing_tag(self, converter):
        """Test can_convert method with non-existing tag."""
        assert converter.can_convert('div') is False
        assert converter.can_convert('span') is False
    
    def test_convert_unknown_tag(self, converter, soup):
        """Test conversion of unknown tag returns text content."""
        html = '<div>Some text</div>'
        tag = BeautifulSoup(html, 'lxml').find('div')
        result = converter.convert(tag)
        assert result == 'Some text'
