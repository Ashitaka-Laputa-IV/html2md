"""Unit tests for TableConverter.

This module tests the conversion of HTML table elements to Markdown.
"""

import pytest
from bs4 import BeautifulSoup
from html2md.converters.table import TableConverter


class TestTableConverter:
    """Test cases for TableConverter class."""
    
    @pytest.fixture
    def converter(self):
        """Create a TableConverter instance for testing."""
        return TableConverter()
    
    def test_convert_simple_table(self, converter):
        """Test conversion of a simple table."""
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
        """Test conversion of a table without header row."""
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
        """Test conversion of a table with thead and tbody."""
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
        """Test conversion of a table with multiple columns."""
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
        """Test conversion of an empty table."""
        html = '<table></table>'
        tag = BeautifulSoup(html, 'lxml').find('table')
        result = converter.convert(tag)
        
        assert result == ""
    
    def test_convert_table_empty_row(self, converter):
        """Test conversion of a table with empty row."""
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
        """Test can_convert method for table tag."""
        assert converter.can_convert('table') is True
        assert converter.can_convert('TABLE') is True
    
    def test_can_convert_table_elements(self, converter):
        """Test can_convert method for table element tags."""
        assert converter.can_convert('thead') is True
        assert converter.can_convert('tbody') is True
        assert converter.can_convert('tr') is True
        assert converter.can_convert('th') is True
        assert converter.can_convert('td') is True
    
    def test_can_convert_non_table_tag(self, converter):
        """Test can_convert method for non-table tags."""
        assert converter.can_convert('div') is False
        assert converter.can_convert('span') is False
        assert converter.can_convert('p') is False
    
    def test_create_separator(self, converter):
        """Test separator creation."""
        separator = converter._create_separator(3)
        assert separator == '| --- | --- | --- |'
        
        separator = converter._create_separator(5)
        assert separator == '| --- | --- | --- | --- | --- |'
    
    def test_get_cell_text(self, converter):
        """Test getting text from table cell."""
        html = '<td>Cell Content</td>'
        cell = BeautifulSoup(html, 'lxml').find('td')
        text = converter._get_cell_text(cell)
        
        assert text == 'Cell Content'
    
    def test_get_cell_text_with_whitespace(self, converter):
        """Test getting text from cell with extra whitespace."""
        html = '<td>  Content with spaces  </td>'
        cell = BeautifulSoup(html, 'lxml').find('td')
        text = converter._get_cell_text(cell)
        
        assert text == 'Content with spaces'
