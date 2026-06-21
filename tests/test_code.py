"""CodeConverter的单元测试。

本模块测试HTML代码元素到Markdown的转换。
"""

import pytest
from bs4 import BeautifulSoup
from html2md.converters.code import CodeConverter


class TestCodeConverter:
    """CodeConverter类的测试用例。"""
    
    @pytest.fixture
    def converter(self):
        """创建CodeConverter实例用于测试。"""
        return CodeConverter()
    
    def test_convert_pre_with_code(self, converter):
        """测试带code子标签的pre标签的转换。"""
        html = '<pre><code>print("Hello")</code></pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```' in result
        assert 'print("Hello")' in result
    
    def test_convert_pre_without_code(self, converter):
        """测试不带code子标签的pre标签的转换。"""
        html = '<pre>Plain text</pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```' in result
        assert 'Plain text' in result
    
    def test_convert_pre_with_language(self, converter):
        """测试带语言类的pre标签的转换。"""
        html = '<pre><code class="language-python">print("Hello")</code></pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```python' in result
        assert 'print("Hello")' in result
    
    def test_convert_pre_with_lang_class(self, converter):
        """测试带lang-类的pre标签的转换。"""
        html = '<pre><code class="lang-javascript">console.log("test")</code></pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        
        assert '```javascript' in result
        assert 'console.log("test")' in result
    
    def test_convert_code_inline(self, converter):
        """测试内联code标签的转换。"""
        html = '<code>inline code</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        
        assert result == '`inline code`'
    
    def test_convert_kbd(self, converter):
        """测试kbd标签的转换。"""
        html = '<kbd>Ctrl</kbd>'
        tag = BeautifulSoup(html, 'lxml').find('kbd')
        result = converter.convert(tag)
        
        assert result == '`Ctrl`'
    
    def test_convert_code_with_special_chars(self, converter):
        """测试带特殊字符的code标签的转换。"""
        html = '<code>if (x > 0) { return x; }</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        
        assert '`if (x > 0) { return x; }`' in result
    
    def test_convert_pre_multiline(self, converter):
        """测试多行代码块的转换。"""
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
        """测试can_convert方法对pre标签的处理。"""
        assert converter.can_convert('pre') is True
        assert converter.can_convert('PRE') is True
    
    def test_can_convert_code(self, converter):
        """测试can_convert方法对code标签的处理。"""
        assert converter.can_convert('code') is True
        assert converter.can_convert('CODE') is True
    
    def test_can_convert_kbd(self, converter):
        """测试can_convert方法对kbd标签的处理。"""
        assert converter.can_convert('kbd') is True
        assert converter.can_convert('KBD') is True
    
    def test_can_convert_non_code_tag(self, converter):
        """测试can_convert方法对非代码标签的处理。"""
        assert converter.can_convert('div') is False
        assert converter.can_convert('span') is False
        assert converter.can_convert('p') is False
    
    def test_get_language_from_class(self, converter):
        """测试从class属性提取语言。"""
        html = '<code class="language-python">code</code>'
        code = BeautifulSoup(html, 'lxml').find('code')
        language = converter._get_language(code)
        
        assert language == 'python'
    
    def test_get_language_from_lang_class(self, converter):
        """测试从lang-类提取语言。"""
        html = '<code class="lang-ruby">code</code>'
        code = BeautifulSoup(html, 'lxml').find('code')
        language = converter._get_language(code)
        
        assert language == 'ruby'
    
    def test_get_language_no_class(self, converter):
        """测试无class属性时提取语言。"""
        html = '<code>code</code>'
        code = BeautifulSoup(html, 'lxml').find('code')
        language = converter._get_language(code)
        
        assert language == ''
    
    def test_get_language_other_class(self, converter):
        """测试其他class属性时提取语言。"""
        html = '<code class="highlight">code</code>'
        code = BeautifulSoup(html, 'lxml').find('code')
        language = converter._get_language(code)
        
        assert language == ''

    # --- 反引号转义测试 ---

    def test_convert_code_with_single_backtick(self, converter):
        """测试内联代码中含单个反引号时的转义。"""
        html = '<code>a ` b</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        assert result == '``a ` b``'

    def test_convert_code_with_double_backticks(self, converter):
        """测试内联代码中含双反引号时的转义。"""
        html = '<code>a `` b</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        assert result == '```a `` b```'

    def test_convert_code_with_triple_backticks(self, converter):
        """测试内联代码中含三反引号时的转义。"""
        html = '<code>a ``` b</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        assert result == '````a ``` b````'

    def test_convert_code_starting_with_backtick(self, converter):
        """测试内联代码以反引号开头时使用空格分隔。"""
        html = '<code>`code`</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        assert result == '`` `code` ``'

    def test_convert_code_ending_with_backtick(self, converter):
        """测试内联代码以反引号结尾时使用空格分隔。"""
        html = '<code>code`</code>'
        tag = BeautifulSoup(html, 'lxml').find('code')
        result = converter.convert(tag)
        assert result == '`` code` ``'

    def test_convert_pre_with_triple_backticks_in_code(self, converter):
        """测试代码块中含三反引号时使用波浪线 fence。"""
        html = '<pre><code>Use ``` like this</code></pre>'
        tag = BeautifulSoup(html, 'lxml').find('pre')
        result = converter.convert(tag)
        assert '~~~' in result
        assert 'Use ``` like this' in result
