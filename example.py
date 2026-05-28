"""html2md库的使用示例。

本脚本演示如何使用HTML2MarkdownConverter将HTML转换为Markdown。
"""

from html2md import HTML2MarkdownConverter


def main():
    """运行示例转换。"""
    converter = HTML2MarkdownConverter()
    
    print("=" * 60)
    print("HTML转Markdown转换器 - 示例")
    print("=" * 60)
    
    # 示例1：简单文档
    html1 = """
    <h1>欢迎使用html2md</h1>
    <p>这是一个<strong>强大</strong>的库，用于将 
    HTML转换为Markdown。</p>
    """
    print("\n1. 简单文档:")
    print("-" * 40)
    print("HTML:")
    print(html1)
    print("\nMarkdown:")
    print(converter.convert(html1))
    
    # 示例2：带列表的文档
    html2 = """
    <h2>功能特性</h2>
    <ul>
        <li>转换基础HTML标签</li>
        <li>支持表格</li>
        <li>支持代码块</li>
        <li>Google风格代码格式化</li>
    </ul>
    """
    print("\n2. 带列表的文档:")
    print("-" * 40)
    print("HTML:")
    print(html2)
    print("\nMarkdown:")
    print(converter.convert(html2))
    
    # 示例3：带表格的文档
    html3 = """
    <h2>对比表格</h2>
    <table>
        <tr>
            <th>功能</th>
            <th>状态</th>
        </tr>
        <tr>
            <td>基础标签</td>
            <td>✓</td>
        </tr>
        <tr>
            <td>表格</td>
            <td>✓</td>
        </tr>
        <tr>
            <td>代码块</td>
            <td>✓</td>
        </tr>
    </table>
    """
    print("\n3. 带表格的文档:")
    print("-" * 40)
    print("HTML:")
    print(html3)
    print("\nMarkdown:")
    print(converter.convert(html3))
    
    # 示例4：带代码的文档
    html4 = """
    <h2>代码示例</h2>
    <p>这是一个Python示例：</p>
    <pre><code class="language-python">def hello_world():
    print("Hello, World!")
    return True</code></pre>
    <p>以及一个内联<code>代码</code>示例。</p>
    """
    print("\n4. 带代码的文档:")
    print("-" * 40)
    print("HTML:")
    print(html4)
    print("\nMarkdown:")
    print(converter.convert(html4))
    
    # 示例5：复杂文档
    html5 = """
    <h1>完整示例</h1>
    <p>本文档演示<strong>所有</strong>功能。</p>
    
    <h2>链接和图片</h2>
    <p>访问<a href="https://example.com" title="示例网站">示例网站</a> 
    获取更多信息。</p>
    <img src="logo.png" alt="Logo" title="公司Logo">
    
    <h2>引用</h2>
    <blockquote>
        这是一段来自重要人物的引用。
        可以跨越多行。
    </blockquote>
    
    <h2>有序列表</h2>
    <ol>
        <li>第一步</li>
        <li>第二步</li>
        <li>第三步</li>
    </ol>
    """
    print("\n5. 复杂文档:")
    print("-" * 40)
    print("HTML:")
    print(html5)
    print("\nMarkdown:")
    print(converter.convert(html5))


if __name__ == "__main__":
    main()
