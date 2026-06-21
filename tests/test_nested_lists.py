"""HTML2MarkdownConverter嵌套列表的单元测试。"""

from html2md import HTML2MarkdownConverter


def test_nested_ul():
    """测试嵌套无序列表的转换。"""
    converter = HTML2MarkdownConverter()
    html = """
    <ul>
        <li>Item 1
            <ul>
                <li>Nested Item 1</li>
                <li>Nested Item 2</li>
            </ul>
        </li>
        <li>Item 2</li>
    </ul>
    """
    result = converter.convert(html)
    assert '- Item 1' in result
    assert '  - Nested Item 1' in result
    assert '  - Nested Item 2' in result
    assert '- Item 2' in result


def test_nested_ol():
    """测试嵌套有序列表的转换。"""
    converter = HTML2MarkdownConverter()
    html = """
    <ol>
        <li>Item 1
            <ol>
                <li>Nested Item 1</li>
                <li>Nested Item 2</li>
            </ol>
        </li>
        <li>Item 2</li>
    </ol>
    """
    result = converter.convert(html)
    assert '1. Item 1' in result
    assert '  1. Nested Item 1' in result
    assert '  2. Nested Item 2' in result
    assert '2. Item 2' in result


def test_mixed_nested_list():
    """测试混合嵌套列表（ul内嵌ol）的转换。"""
    converter = HTML2MarkdownConverter()
    html = """
    <ul>
        <li>Item 1
            <ol>
                <li>Nested Ordered 1</li>
                <li>Nested Ordered 2</li>
            </ol>
        </li>
        <li>Item 2</li>
    </ul>
    """
    result = converter.convert(html)
    assert '- Item 1' in result
    assert '  1. Nested Ordered 1' in result
    assert '  2. Nested Ordered 2' in result
    assert '- Item 2' in result


# 保留原手动运行入口
if __name__ == "__main__":
    test_nested_ul()
    test_nested_ol()
    test_mixed_nested_list()
    print("所有嵌套列表测试通过")
