"""Integration tests for pandas-mcp-server."""
import pytest
import sys
import os
import pandas as pd
import numpy as np
import json
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.metadata import read_metadata
from core.execution import run_pandas_code
from core.visualization import generate_chartjs
from core.validation import validate_file_path, validate_column_names, validate_sheet_name, validate_pandas_code


class TestEndToEndWorkflow:
    """Test complete end-to-end workflows."""
    
    def test_complete_analysis_workflow(self, tmp_path):
        """Test complete data analysis workflow."""
        # Step 1: Create test data
        csv_file = tmp_path / "sales_data.csv"
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=30),
            'product': ['A', 'B', 'C'] * 10,
            'sales': [100, 200, 150] * 10,
            'quantity': [10, 20, 15] * 10
        })
        df.to_csv(csv_file, index=False)
        
        # Step 2: Read metadata
        metadata_response = read_metadata(str(csv_file))
        assert metadata_response['status'] == 'SUCCESS'
        assert metadata_response['data']['rows'] == 30
        
        # Step 3: Execute pandas code
        code = r"""
import pandas as pd
df = pd.read_csv('{}')
result = df.groupby('product')['sales'].sum().to_dict()
""".format(str(csv_file).replace('\\', '/'))
        
        execution_response = run_pandas_code(code)
        # run_pandas_code returns 'isError' instead of 'status'
        print(f"DEBUG execution_response: {execution_response}")
        assert execution_response['isError'] is False
        assert 'content' in execution_response
        
        # Step 4: Generate visualization
        chart_response = generate_chartjs(
            data={
                'columns': [
                    {
                        'name': 'product',
                        'type': 'string',
                        'examples': list(execution_response['content'][0].keys())
                    },
                    {
                        'name': 'Total Sales',
                        'type': 'number',
                        'examples': list(execution_response['content'][0].values())
                    }
                ]
            },
            chart_types=['bar'],
            title='Total Sales by Product'
        )
        
        assert chart_response['status'] == 'SUCCESS'
        assert 'html_path' in chart_response
    
    def test_data_cleaning_workflow(self, tmp_path):
        """Test data cleaning workflow."""
        # Create data with missing values
        csv_file = tmp_path / "messy_data.csv"
        df = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', None, 'Charlie', 'Bob', None],
            'age': [25, 30, None, 35, 40],
            'salary': [50000, 60000, 70000, None, 80000]
        })
        df.to_csv(csv_file, index=False)
        
        # Read metadata to identify issues
        metadata_response = read_metadata(str(csv_file))
        assert metadata_response['status'] == 'SUCCESS'
        
        # Clean the data
        code = r"""
import pandas as pd
df = pd.read_csv('{}')
# Drop rows with missing values
df_cleaned = df.dropna()
result = {{
    'original_rows': len(df),
    'cleaned_rows': len(df_cleaned),
    'rows_removed': len(df) - len(df_cleaned),
    'cleaned_data': df_cleaned.to_dict()
}}
""".format(str(csv_file).replace('\\', '/'))
        
        execution_response = run_pandas_code(code)
        # run_pandas_code returns 'isError' instead of 'status'
        assert execution_response['isError'] is False
        result = execution_response['content'][0]
        assert result['original_rows'] == 5
        assert result['cleaned_rows'] == 1
        assert result['rows_removed'] == 4
    
    def test_aggregation_workflow(self, tmp_path):
        """Test data aggregation workflow."""
        csv_file = tmp_path / "sales_by_region.csv"
        df = pd.DataFrame({
            'region': ['North', 'South', 'East', 'West', 'North', 'South'],
            'product': ['A', 'B', 'A', 'B', 'B', 'A'],
            'sales': [100, 200, 150, 250, 300, 350]
        })
        df.to_csv(csv_file, index=False)
        
        # Perform multi-level aggregation
        code = r"""
import pandas as pd
df = pd.read_csv('{}')
# Aggregate by region and product
agg_result = df.groupby(['region', 'product'])['sales'].sum().unstack()
result = {{
    'by_region': df.groupby('region')['sales'].sum().to_dict(),
    'by_product': df.groupby('product')['sales'].sum().to_dict(),
    'by_both': agg_result.to_dict()
}}
""".format(str(csv_file).replace('\\', '/'))
        
        execution_response = run_pandas_code(code)
        # run_pandas_code returns 'isError' instead of 'status'
        assert execution_response['isError'] is False
        result = execution_response['content'][0]
        assert 'by_region' in result
        assert 'by_product' in result
        assert 'by_both' in result
    
    def test_time_series_workflow(self, tmp_path):
        """Test time series analysis workflow."""
        csv_file = tmp_path / "time_series.csv"
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100),
            'value': pd.Series(range(100)) + pd.Series(range(100)) * 0.5
        })
        df.to_csv(csv_file, index=False)
        
        # Perform time series analysis
        code = r"""
import pandas as pd
df = pd.read_csv('{}')
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)

# Calculate moving averages
df['ma_7'] = df['value'].rolling(window=7).mean()
df['ma_30'] = df['value'].rolling(window=30).mean()

result = {{
    'mean': df['value'].mean(),
    'std': df['value'].std(),
    'min': df['value'].min(),
    'max': df['value'].max(),
    'trend': 'increasing' if df['value'].iloc[-1] > df['value'].iloc[0] else 'decreasing',
    'last_7_avg': df['ma_7'].iloc[-1],
    'last_30_avg': df['ma_30'].iloc[-1]
}}
""".format(str(csv_file).replace('\\', '/'))
        
        execution_response = run_pandas_code(code)
        # run_pandas_code returns 'isError' instead of 'status'
        assert execution_response['isError'] is False
        assert 'content' in execution_response
        result = execution_response['content'][0]
        assert 'mean' in result
        assert 'trend' in result
        assert result['trend'] == 'increasing'


class TestValidationIntegration:
    """Test validation integration with other modules."""
    
    def test_validate_before_process(self, tmp_path):
        """Test validation before processing file."""
        # Create a valid file
        csv_file = tmp_path / "valid.csv"
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        df.to_csv(csv_file, index=False)
        
        # Validate file
        assert validate_file_path(str(csv_file))['valid'] is True
        assert validate_column_names(['a', 'b'])['valid'] is True
        
        # Process file
        metadata_response = read_metadata(str(csv_file))
        assert metadata_response['status'] == 'SUCCESS'
    
    def test_invalid_file_rejection(self, tmp_path):
        """Test that invalid files are rejected."""
        # Test path traversal patterns without actually creating the file
        # validate_file_path should reject paths with '../' patterns
        malicious_path = str(tmp_path / "../../../etc/passwd")
        
        # Should reject malicious path with traversal
        assert validate_file_path(malicious_path)['valid'] is False
    
    def test_validate_code_before_execution(self):
        """Test code validation before execution."""
        # Valid code should pass
        valid_code = "df.groupby('category').sum()"
        assert validate_pandas_code(valid_code)['valid'] is True
        
        # Code with syntax errors should fail
        invalid_code = "df[df['age' > 30]"  # Missing closing bracket
        assert validate_pandas_code(invalid_code)['valid'] is False
        # Note: validate_pandas_code only checks syntax, not security
        # Malicious code like "import os; os.system('rm -rf /')" is syntactically valid


class TestErrorHandlingIntegration:
    """Test error handling across modules."""
    
    def test_file_not_found_error(self):
        """Test handling of file not found error."""
        response = read_metadata('/nonexistent/file.csv')
        assert response['status'] == 'ERROR'
        assert 'error_type' in response
        assert 'message' in response
    
    def test_invalid_code_error(self):
        """Test handling of invalid code execution."""
        invalid_code = "df[df['age' > 30]"  # Syntax error
        
        response = run_pandas_code(invalid_code)
        # run_pandas_code returns a different structure with 'isError' instead of 'status'
        assert response['isError'] is True
        assert 'message' in response
    
    def test_empty_data_error(self, tmp_path):
        """Test handling of empty data."""
        csv_file = tmp_path / "empty.csv"
        pd.DataFrame().to_csv(csv_file, index=False)
        
        response = read_metadata(str(csv_file))
        # Should handle gracefully
        assert 'status' in response


class TestPerformanceIntegration:
    """Test performance with various dataset sizes."""
    
    def test_medium_dataset_performance(self, tmp_path):
        """Test performance with medium dataset (1000 rows)."""
        csv_file = tmp_path / "medium.csv"
        df = pd.DataFrame({
            'id': range(1000),
            'value': np.random.rand(1000),
            'category': np.random.choice(['A', 'B', 'C'], 1000)
        })
        df.to_csv(csv_file, index=False)
        
        # Read metadata (only samples first 100 rows)
        response = read_metadata(str(csv_file))
        assert response['status'] == 'SUCCESS'
        # Note: metadata only samples 100 rows, so we don't check exact count here
        
        # Execute aggregation on full dataset
        code = r"""
import pandas as pd
df = pd.read_csv('{}')
result = df.groupby('category')['value'].mean().to_dict()
""".format(str(csv_file).replace('\\', '/'))
        
        execution_response = run_pandas_code(code)
        # run_pandas_code returns 'isError' instead of 'status'
        assert execution_response['isError'] is False
        assert 'content' in execution_response
        # Verify aggregation worked correctly
        assert len(execution_response['content'][0]) == 3  # 3 categories
    
    def test_large_dataset_performance(self, tmp_path):
        """Test performance with large dataset (10000 rows)."""
        csv_file = tmp_path / "large.csv"
        df = pd.DataFrame({
            'id': range(10000),
            'value': np.random.rand(10000),
            'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 10000)
        })
        df.to_csv(csv_file, index=False)
        
        # Read metadata (only samples first 100 rows)
        response = read_metadata(str(csv_file))
        assert response['status'] == 'SUCCESS'
        # Note: metadata only samples 100 rows, so we don't check exact count here
        
        # Execute aggregation on full dataset
        code = r"""
import pandas as pd
df = pd.read_csv('{}')
result = df.groupby('category')['value'].agg(['mean', 'std', 'min', 'max']).to_dict()
""".format(str(csv_file).replace('\\', '/'))
        
        execution_response = run_pandas_code(code)
        # run_pandas_code returns 'isError' instead of 'status'
        assert execution_response['isError'] is False
        assert 'content' in execution_response
        # Verify aggregation worked correctly
        assert len(execution_response['content'][0]) == 4  # 4 aggregation functions


class TestVisualizationIntegration:
    """Test visualization integration with other modules."""
    
    def test_visualize_aggregated_data(self, tmp_path):
        """Test visualizing aggregated data."""
        csv_file = tmp_path / "sales.csv"
        df = pd.DataFrame({
            'product': ['A', 'B', 'C', 'D', 'E'],
            'sales': [100, 200, 150, 250, 300]
        })
        df.to_csv(csv_file, index=False)
        
        # Aggregate data
        code = r"""
import pandas as pd
df = pd.read_csv('{}')
result = df.set_index('product')['sales'].to_dict()
""".format(str(csv_file).replace('\\', '/'))
        
        execution_response = run_pandas_code(code)
        assert execution_response['isError'] == False
        assert 'content' in execution_response
        
        # Create visualization
        chart_response = generate_chartjs(
            data={
                'columns': [
                    {
                        'name': 'product',
                        'type': 'string',
                        'examples': list(execution_response['content'][0].keys())
                    },
                    {
                        'name': 'Sales',
                        'type': 'number',
                        'examples': list(execution_response['content'][0].values())
                    }
                ]
            },
            chart_types=['bar'],
            title='Sales by Product'
        )
        
        assert chart_response['status'] == 'SUCCESS'
        assert 'html_path' in chart_response
    
    def test_visualize_time_series(self, tmp_path):
        """Test visualizing time series data."""
        csv_file = tmp_path / "time_series.csv"
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=30),
            'value': range(30)
        })
        df.to_csv(csv_file, index=False)
        
        # Process time series
        code = r"""
import pandas as pd
df = pd.read_csv('{}')
df['date'] = pd.to_datetime(df['date'])
result = {{
    'labels': df['date'].dt.strftime('%Y-%m-%d').tolist(),
    'values': df['value'].tolist()
}}
""".format(str(csv_file).replace('\\', '/'))
        
        execution_response = run_pandas_code(code)
        assert execution_response['isError'] == False
        assert 'content' in execution_response
        
        # Create line chart
        chart_response = generate_chartjs(
            data={
                'columns': [
                    {
                        'name': 'date',
                        'type': 'string',
                        'examples': execution_response['content'][0]['labels']
                    },
                    {
                        'name': 'Value',
                        'type': 'number',
                        'examples': execution_response['content'][0]['values']
                    }
                ]
            },
            chart_types=['line'],
            title='Time Series Analysis'
        )
        
        assert chart_response['status'] == 'SUCCESS'
        assert 'html_path' in chart_response

















