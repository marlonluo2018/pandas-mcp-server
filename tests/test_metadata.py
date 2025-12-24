"""Unit tests for metadata module."""
import pytest
import sys
import os
import pandas as pd
import numpy as np

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.metadata import read_metadata, process_sheet
from core.error_handling import ErrorType


class TestReadMetadata:
    """Test read_metadata function."""
    
    def test_csv_metadata(self, tmp_path):
        """Test reading metadata from CSV file."""
        # Create a test CSV file
        csv_file = tmp_path / "test.csv"
        df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35],
            'salary': [50000.0, 60000.0, 70000.0]
        })
        df.to_csv(csv_file, index=False)
        
        response = read_metadata(str(csv_file))
        
        assert response['status'] == 'SUCCESS'
        assert response['file_info']['type'] == 'csv'
        assert 'data' in response
        assert response['data']['rows'] == 3
        assert len(response['data']['columns']) == 4
    
    def test_excel_metadata(self, tmp_path):
        """Test reading metadata from Excel file."""
        # Create a test Excel file
        excel_file = tmp_path / "test.xlsx"
        df = pd.DataFrame({
            'product': ['A', 'B', 'C'],
            'quantity': [10, 20, 30],
            'price': [100.0, 200.0, 300.0]
        })
        df.to_excel(excel_file, index=False)
        
        response = read_metadata(str(excel_file))
        
        assert response['status'] == 'SUCCESS'
        assert response['file_info']['type'] == 'excel'
        assert 'data' in response
        assert 'sheets' in response['data']
        assert len(response['data']['sheets']) == 1
    
    def test_column_dtypes(self, tmp_path):
        """Test column data type detection."""
        csv_file = tmp_path / "test_dtypes.csv"
        df = pd.DataFrame({
            'int_col': [1, 2, 3],
            'float_col': [1.1, 2.2, 3.3],
            'str_col': ['a', 'b', 'c'],
            'bool_col': [True, False, True]
        })
        df.to_csv(csv_file, index=False)
        
        response = read_metadata(str(csv_file))
        
        assert response['status'] == 'SUCCESS'
        
        # Check that columns are detected
        column_names = [col['name'] for col in response['data']['columns']]
        assert 'int_col' in column_names
        assert 'float_col' in column_names
        assert 'str_col' in column_names
        assert 'bool_col' in column_names
    
    def test_missing_values_detection(self, tmp_path):
        """Test detection of missing values."""
        csv_file = tmp_path / "test_missing.csv"
        df = pd.DataFrame({
            'col1': [1, None, 3],
            'col2': ['a', None, 'c'],
            'col3': [1.0, 2.0, None]
        })
        df.to_csv(csv_file, index=False)
        
        response = read_metadata(str(csv_file))
        
        assert response['status'] == 'SUCCESS'
        
        # Check for missing values in columns
        for col in response['data']['columns']:
            assert 'stats' in col
            assert 'null_count' in col['stats']
    
    def test_file_not_found(self):
        """Test handling of non-existent file."""
        response = read_metadata('/nonexistent/file.csv')
        
        assert response['status'] == 'ERROR'
        assert 'error_type' in response
        assert 'message' in response
    
    def test_directory_path(self, tmp_path):
        """Test handling of directory path."""
        response = read_metadata(str(tmp_path))
        
        assert response['status'] == 'ERROR'
        assert 'error_type' in response
        assert 'message' in response
    
    def test_empty_dataframe(self, tmp_path):
        """Test handling of empty file."""
        csv_file = tmp_path / "empty.csv"
        df = pd.DataFrame()
        df.to_csv(csv_file, index=False)
        
        response = read_metadata(str(csv_file))
        
        # Should handle gracefully
        assert 'status' in response


class TestProcessSheet:
    """Test process_sheet function."""
    
    def test_basic_dataframe(self):
        """Test processing a basic DataFrame."""
        df = pd.DataFrame({
            'name': ['Alice', 'Bob', 'Charlie'],
            'age': [25, 30, 35]
        })
        
        result = process_sheet(df)
        
        assert result['rows'] == 3
        assert result['cols'] == 2
        assert len(result['columns']) == 2
        
        # Check column structure
        for col in result['columns']:
            assert 'name' in col
            assert 'type' in col
            assert 'examples' in col
            assert 'stats' in col
    
    def test_empty_dataframe(self):
        """Test processing an empty DataFrame."""
        df = pd.DataFrame()
        
        result = process_sheet(df)
        
        assert result['rows'] == 0
        assert result['cols'] == 0
        assert len(result['columns']) == 0
    
    def test_dataframe_with_nulls(self):
        """Test processing DataFrame with null values."""
        df = pd.DataFrame({
            'col1': [1, None, 3],
            'col2': [None, None, None]
        })
        
        result = process_sheet(df)
        
        assert result['rows'] == 3
        assert result['cols'] == 2
        
        # Check that null_count is tracked
        for col in result['columns']:
            assert 'stats' in col
            assert 'null_count' in col['stats']
    
    def test_numeric_column_stats(self):
        """Test that numeric columns get appropriate stats."""
        df = pd.DataFrame({
            'numeric': [1.0, 2.0, 3.0, 4.0, 5.0]
        })
        
        result = process_sheet(df)
        
        assert len(result['columns']) == 1
        col = result['columns'][0]
        assert col['name'] == 'numeric'
        assert 'stats' in col
        assert 'null_count' in col['stats']
        assert 'unique_count' in col['stats']


class TestMetadataStructure:
    """Test the structure of metadata responses."""
    
    def test_csv_response_structure(self, tmp_path):
        """Test that CSV response has correct structure."""
        csv_file = tmp_path / "test_structure.csv"
        df = pd.DataFrame({'col1': [1, 2, 3]})
        df.to_csv(csv_file, index=False)
        
        result = read_metadata(str(csv_file))
        
        assert result['status'] == 'SUCCESS'
        assert 'file_info' in result
        assert 'data' in result
        assert 'rows' in result['data']
        assert 'columns' in result['data']
    
    def test_excel_response_structure(self, tmp_path):
        """Test that Excel response has correct structure."""
        excel_file = tmp_path / "test_structure.xlsx"
        df = pd.DataFrame({'col1': [1, 2, 3]})
        df.to_excel(excel_file, index=False)
        
        result = read_metadata(str(excel_file))
        
        # Check top-level structure
        assert 'status' in result
        assert 'file_info' in result
        assert 'data' in result
        
        # Check file_info structure
        assert 'type' in result['file_info']
        assert 'sheet_count' in result['file_info']
        assert 'sheet_names' in result['file_info']
        
        # Check data structure
        assert 'sheets' in result['data']
    
    def test_column_metadata_format(self, tmp_path):
        """Test that column metadata has correct format."""
        csv_file = tmp_path / "test_col_format.csv"
        df = pd.DataFrame({'test_col': [1, 2, 3]})
        df.to_csv(csv_file, index=False)
        
        result = read_metadata(str(csv_file))
        
        # Check column structure
        assert len(result['data']['columns']) > 0
        col = result['data']['columns'][0]
        
        # Check required fields
        assert 'name' in col
        assert 'type' in col
        assert 'examples' in col
        assert 'stats' in col
        
        # Check stats structure
        assert 'null_count' in col['stats']
        assert 'unique_count' in col['stats']