# HTML2MD

一个用于将HTML转换为Markdown的Python库。

## 安装

```bash
pip install html2md
```

## 使用方法

```python
from html2md import HTML2MarkdownConverter

html = "<h1>Hello World</h1>"
converter = HTML2MarkdownConverter()
markdown = converter.convert(html)
print(markdown)  # 输出: # Hello World
```

## 功能特性

- 转换基础HTML标签（标题、段落、粗体、斜体、链接、图片、列表）
- 支持HTML表格
- 支持代码块
- 完整的单元测试

## 开发

```bash
pip install -e .[dev]
pytest
```
