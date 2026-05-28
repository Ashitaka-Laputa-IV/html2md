"""测试嵌套列表的实际输出。"""

from html2md.converter import HTML2MarkdownConverter


def test_nested_lists():
    """测试各种嵌套列表。"""
    converter = HTML2MarkdownConverter()
    
    # 测试1: 嵌套无序列表
    html1 = """
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
    result1 = converter.convert(html1)
    print("测试1: 嵌套无序列表")
    print("期望输出:")
    print("- Item 1")
    print("  - Nested Item 1")
    print("  - Nested Item 2")
    print("- Item 2")
    print("\n实际输出:")
    print(result1)
    print("="*50 + "\n")
    
    # 测试2: 嵌套有序列表
    html2 = """
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
    result2 = converter.convert(html2)
    print("测试2: 嵌套有序列表")
    print("期望输出:")
    print("1. Item 1")
    print("  1. Nested Item 1")
    print("  2. Nested Item 2")
    print("2. Item 2")
    print("\n实际输出:")
    print(result2)
    print("="*50 + "\n")
    
    # 测试3: 混合嵌套列表
    html3 = """
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
    result3 = converter.convert(html3)
    print("测试3: 混合嵌套列表")
    print("期望输出:")
    print("- Item 1")
    print("  1. Nested Ordered 1")
    print("  2. Nested Ordered 2")
    print("- Item 2")
    print("\n实际输出:")
    print(result3)


if __name__ == "__main__":
    test_nested_lists()
