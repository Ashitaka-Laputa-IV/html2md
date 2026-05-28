"""Unit tests for CodeConverter.

This module tests the conversion of HTML code elements to Markdown.
"""

import pytest
from bs4 import BeautifulSoup
from html2md.converters.code import CodeConverter


class TestCodeConverter:
    """Test cases for CodeConverter class."""
    
    @pytest.fixture
    def converter(self):
        """Create a CodeConverter instance for testing."""
        return CodeConverter()
    
    def test_convert_pre_with_code(self, converter):
        """Test conversion of pre tag with code child."""
        html = '<pre><code>print("Hello")</code></pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```' in result
        assert 'print("Hello")' in result
    
    def test_convert_pre_without_code(self, converter):
        """Test conversion of pre tag without code child."""
        html = '<pre>Plain text</pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```' in result
        assert 'Plain text' in result
    
    def test_convert_pre_with_language(self, converter):
        """Test conversion of pre tag with language class."""
        html = '<pre><code class="language-python">print("Hello")</code></pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```python' in result
        assert 'print("Hello")' in result
    
    def test_convert_pre_with_lang_class(self, converter):
        """Test conversion of pre tag with lang- class."""
        html = '<pre><code class="lang-javascript">console.log("test")</code></pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```javascript' in result
        assert 'console.log("test")' in result
    
    def test_convert_code_inline(self, converter):
        """Test conversion of inline code tag."""
        html = '<code>inline code</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        
        assert result == '`inline code`'
    
    def test_convert_kbd(self, converter):
        """Test conversion of kbd tag."""
        html = '<kbd>Ctrl</kbd>'
        tag = BeautifulSoup(html, 'lxml').find('kbd')
        result = converter.convert(tag)
        
        assert result == '`Ctrl`'
    
    def test_convert_code_with_special_chars(self, converter):
        """Test conversion of code with special characters."""
        html = '<code>if (x > 0) { return x; }</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        
        assert '`if (x > 0) { return x; }`' in result
    
    def test_convert_pre_multiline(self, converter):
        """Test conversion of multiline code block."""
        html = '''<pre><code>def hello():
    print("World")
    return True</code></pre>'''
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```' in result
        assert 'def hello():' in result
        assert 'print("World")' in result
        assert 'return True' in result
    
    def test_can_convert_pre(self, converter):
        """Test can_convert method for pre tag."""
        assert converter.can_convert('pre') is True
        assert converter.can_convert('PRE') is True
    
    def test_can_convert_code(self, converter):
        """Test can_convert method for code tag."""
        assert converter.can_convert('code') is True
        assert converter.can_convert('CODE') is True
    
    def test_can_convert_kbd(self, converter):
        """Test can_convert method for kbd tag."""
        assert converter.can_convert('kbd') is True
        assert converter.can_convert('KBD') is True
    
    def test_can_convert_non_code_tag(self, converter):
        """Test can_convert method for non-code tags."""
        assert converter.can_convert('div') is False
        assert converter.can_convert('span') is False
        assert converter.can_convert('p') is False
    
    def test_get_language_from_class(self, converter):
        """Test extracting language from class attribute."""
        html = '<code class="language-python">code</code>'
        code = BeautifulSoup(html, 'lxml').find('code')
        language = converter._get_language(code)
        
        assert language == 'python'
    
    def test_get_language_from_lang_class(self, converter):
        """Test extracting language from lang- class."""
        html = '<code class="lang-ruby">code</code>'
        code = BeautifulSoup(html, 'lxml').find('code')
        language = converter._get_language(code)
        
        assert language == 'ruby'
    
    def test_get_language_no_class(self, converter):
        """Test extracting language when no class present."""
        html = '<code>code</code>'
        code = BeautifulSoup(html, 'lxml').find('code')
        language = converter._get_language(code)
        
        assert language == ''
    
    def test_get_language_other_class(self, converter):
        """Test extracting language when other class present."""
        html = '<code class="highlight">code</code>'
        code = BeautifulSoup(html, 'lxml').find('code')
        language = converter._get_language(code)
        
        assert language == ''
