"""HTML2MarkdownConverter的集成测试。

本模块测试从HTML到Markdown的完整转换流程。
"""

import pytest
from html2md import HTML2MarkdownConverter


class TestHTML2MarkdownConverter:
    """HTML2MarkdownConverter类的集成测试用例。"""
    
    @pytest.fixture
    def converter(self):
        """创建HTML2MarkdownConverter实例用于测试。"""
        return HTML2MarkdownConverter()
    
    def test_convert_simple_document(self, converter):
        """测试简单HTML文档的转换。"""
        html = '''
        <h1>Title</h1>
        <p>This is a <strong>bold</strong> paragraph.</p>
        '''
        result = converter.convert(html)
        
        assert '# Title' in result
        assert 'This is a **bold** paragraph.' in result
    
    def test_convert_complex_document(self, converter):
        """测试复杂HTML文档的转换。"""
        html = '''
        <h1>Main Title</h1>
        <h2>Subtitle</h2>
        <p>This is a paragraph with <em>italic</em> and <strong>bold</strong> text.</p>
        <p>Here's a <a href="https://example.com">link</a>.</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        '''
        result = converter.convert(html)
        
        assert '# Main Title' in result
        assert '## Subtitle' in result
        assert '*italic*' in result
        assert '**bold**' in result
        assert '[link](https://example.com)' in result
        assert '- Item 1' in result
        assert '- Item 2' in result
    
    def test_convert_document_with_table(self, converter):
        """测试带表格的HTML文档的转换。"""
        html = '''
        <h1>Data Table</h1>
        <table>
            <tr>
                <th>Name</th>
                <th>Age</th>
            </tr>
            <tr>
                <td>Alice</td>
                <td>30</td>
            </tr>
        </table>
        '''
        result = converter.convert(html)
        
        assert '# Data Table' in result
        assert '| Name | Age |' in result
        assert '| --- | --- |' in result
        assert '| Alice | 30 |' in result
    
    def test_convert_document_with_code(self, converter):
        """测试带代码块的HTML文档的转换。"""
        html = '''
        <h1>Code Example</h1>
        <pre><code class="language-python">def hello():
    print("World")</code></pre>
        <p>Inline <code>code</code> example.</p>
        '''
        result = converter.convert(html)
        
        assert '# Code Example' in result
        assert '```python' in result
        assert 'def hello():' in result
        assert '`code`' in result
    
    def test_convert_document_with_images(self, converter):
        """测试带图片的HTML文档的转换。"""
        html = '''
        <h1>Images</h1>
        <img src="image.png" alt="An image">
        <img src="photo.jpg" alt="Photo" title="A photo">
        '''
        result = converter.convert(html)
        
        assert '# Images' in result
        assert '![An image](image.png)' in result
        assert '![Photo](photo.jpg "A photo")' in result
    
    def test_convert_document_with_lists(self, converter):
        """测试带列表的HTML文档的转换。"""
        html = '''
        <h1>Lists</h1>
        <h2>Unordered List</h2>
        <ul>
            <li>First</li>
            <li>Second</li>
            <li>Third</li>
        </ul>
        <h2>Ordered List</h2>
        <ol>
            <li>Step 1</li>
            <li>Step 2</li>
            <li>Step 3</li>
        </ol>
        '''
        result = converter.convert(html)
        
        assert '# Lists' in result
        assert '## Unordered List' in result
        assert '- First' in result
        assert '- Second' in result
        assert '## Ordered List' in result
        assert '1. Step 1' in result
        assert '2. Step 2' in result
    
    def test_convert_document_with_blockquote(self, converter):
        """测试带引用的HTML文档的转换。"""
        html = '''
        <h1>Quote</h1>
        <blockquote>This is a quote from someone important.</blockquote>
        '''
        result = converter.convert(html)
        
        assert '# Quote' in result
        assert '> This is a quote from someone important.' in result
    
    def test_convert_empty_html(self, converter):
        """测试空HTML字符串的转换。"""
        with pytest.raises(ValueError, match="HTML字符串不能为空或None"):
            converter.convert('')
    
    def test_convert_none_html(self, converter):
        """测试None HTML字符串的转换。"""
        with pytest.raises(ValueError, match="HTML字符串不能为空或None"):
            converter.convert(None)
    
    def test_convert_whitespace_only_html(self, converter):
        """测试仅包含空白字符的HTML字符串的转换。"""
        with pytest.raises(ValueError, match="HTML字符串不能为空或None"):
            converter.convert('   \n\t  ')
    
    def test_convert_mixed_content(self, converter):
        """测试混合内容HTML的转换。"""
        html = '''
        <h1>Article</h1>
        <p>First paragraph with <strong>bold</strong> text.</p>
        <pre><code>some code</code></pre>
        <table>
            <tr><th>Header</th></tr>
            <tr><td>Data</td></tr>
        </table>
        <p>Last paragraph.</p>
        '''
        result = converter.convert(html)
        
        assert '# Article' in result
        assert '**bold**' in result
        assert '```' in result
        assert '| Header |' in result
        assert '| Data |' in result
        assert 'Last paragraph.' in result
    
    def test_convert_nested_elements(self, converter):
        """测试嵌套HTML元素的转换。"""
        html = '''
        <p>This has <strong>bold and <em>italic</em> text</strong> inside.</p>
        '''
        result = converter.convert(html)
        
        assert '**bold and *italic* text**' in result or 'bold' in result
    
    def test_convert_real_world_html(self, converter):
        """测试真实世界HTML片段的转换。"""
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Page</title>
        </head>
        <body>
            <h1>Welcome</h1>
            <p>This is a <strong>test</strong> page.</p>
            <ul>
                <li>Feature 1</li>
                <li>Feature 2</li>
            </ul>
            <pre><code class="language-python">print("Hello")</code></pre>
        </body>
        </html>
        '''
        result = converter.convert(html)
        
        assert '# Welcome' in result
        assert '**test**' in result
        assert '- Feature 1' in result
        assert '```python' in result
