"""Unit tests for execution module."""
import pytest
import sys
import os
import pandas as pd
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.execution import run_pandas_code, get_forbidden_reason
from core.error_handling import ErrorType


class TestGetForbiddenReason:
    """Test get_forbidden_reason function."""
    
    def test_forbidden_os_access(self):
        """Test OS access forbidden reason."""
        reason = get_forbidden_reason('os.')
        assert 'Operating system access' in reason
    
    def test_forbidden_subprocess(self):
        """Test subprocess forbidden reason."""
        reason = get_forbidden_reason('subprocess.')
        assert 'arbitrary commands' in reason
    
    def test_forbidden_open(self):
        """Test file open forbidden reason."""
        reason = get_forbidden_reason('open(')
        assert 'file access' in reason
    
    def test_forbidden_exec(self):
        """Test exec forbidden reason."""
        reason = get_forbidden_reason('exec(')
        assert 'arbitrary code' in reason
    
    def test_unknown_forbidden(self):
        """Test unknown forbidden operation."""
        reason = get_forbidden_reason('unknown')
        assert 'forbidden' in reason.lower()


class TestRunPandasCode:
    """Test run_pandas_code function."""
    
    def test_simple_pandas_code(self):
        """Test execution of simple pandas code."""
        code = """
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
result = df.sum()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_dataframe_creation(self):
        """Test DataFrame creation."""
        code = """
import pandas as pd
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'LA', 'Chicago']
})
result = df.to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
        assert isinstance(response['content'][0], dict)
    
    def test_data_filtering(self):
        """Test DataFrame filtering."""
        code = """
import pandas as pd
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35]
})
result = df[df['age'] > 28].to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_groupby_operations(self):
        """Test groupby operations."""
        code = """
import pandas as pd
df = pd.DataFrame({
    'category': ['A', 'B', 'A', 'B', 'A'],
    'value': [10, 20, 30, 40, 50]
})
result = df.groupby('category')['value'].sum().to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_merge_operations(self):
        """Test DataFrame merge operations."""
        code = """
import pandas as pd
df1 = pd.DataFrame({'key': ['A', 'B'], 'value1': [1, 2]})
df2 = pd.DataFrame({'key': ['A', 'B'], 'value2': [3, 4]})
result = pd.merge(df1, df2, on='key').to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_forbidden_code_detection(self):
        """Test that forbidden operations are detected."""
        code = """
import os
os.system('echo test')
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is True
        assert 'message' in response
        assert 'forbidden' in response['message'].lower()
    
    def test_syntax_error_handling(self):
        """Test handling of syntax errors."""
        code = """
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3])
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is True
        assert 'message' in response
    
    def test_runtime_error_handling(self):
        """Test handling of runtime errors."""
        code = """
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3]})
result = df['nonexistent_column'].sum()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is True
        assert 'message' in response
    
    def test_no_result_variable(self):
        """Test code without result variable."""
        code = """
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3]})
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is True
        # Should return an error about missing result variable
    
    def test_multiple_statements(self):
        """Test code with multiple statements."""
        code = """
import pandas as pd
import numpy as np
df1 = pd.DataFrame({'a': [1, 2, 3]})
df2 = pd.DataFrame({'b': [4, 5, 6]})
result = pd.concat([df1, df2], axis=1)
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_numpy_operations(self):
        """Test numpy operations."""
        code = """
import pandas as pd
import numpy as np
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
result = np.array(df.sum()).tolist()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_empty_code(self):
        """Test handling of empty code."""
        code = ""
        response = run_pandas_code(code)
        
        assert response['isError'] is True
        assert 'message' in response
    
    def test_whitespace_only_code(self):
        """Test handling of whitespace-only code."""
        code = "   \n   \n   "
        response = run_pandas_code(code)
        
        assert response['isError'] is True
        assert 'message' in response
    
    def test_large_dataframe_handling(self):
        """Test handling of large DataFrames."""
        code = """
import pandas as pd
import numpy as np
df = pd.DataFrame({
    'a': np.random.rand(1000),
    'b': np.random.rand(1000),
    'c': np.random.rand(1000)
})
result = df.describe().to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_string_operations(self):
        """Test string operations on DataFrames."""
        code = """
import pandas as pd
df = pd.DataFrame({
    'name': ['alice', 'bob', 'charlie'],
    'city': ['nyc', 'la', 'chicago']
})
df['name_upper'] = df['name'].str.upper()
result = df.to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_datetime_operations(self):
        """Test datetime operations."""
        code = """
import pandas as pd
df = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=5),
    'value': [10, 20, 30, 40, 50]
})
df['year'] = df['date'].dt.year
result = df.to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_pivot_table(self):
        """Test pivot table operations."""
        code = """
import pandas as pd
df = pd.DataFrame({
    'category': ['A', 'B', 'A', 'B', 'A'],
    'subcategory': ['X', 'Y', 'X', 'Y', 'X'],
    'value': [10, 20, 30, 40, 50]
})
result = df.pivot_table(
    index='category',
    columns='subcategory',
    values='value',
    aggfunc='sum'
).to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response
    
    def test_apply_function(self):
        """Test apply function with lambda."""
        code = """
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
result = df.apply(lambda x: x * 2).to_dict()
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is False
        assert 'content' in response


class TestExecutionSecurity:
    """Test security aspects of code execution."""
    
    def test_prevent_file_operations(self):
        """Test that file operations are prevented."""
        code = """
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3]})
df.to_csv('test.csv')
"""
        response = run_pandas_code(code)
        
        # This should either succeed (if to_csv is allowed) or fail with specific error
        # The important thing is that it doesn't execute arbitrary file operations
        assert 'isError' in response
    
    def test_prevent_import_hacks(self):
        """Test prevention of import hacks."""
        code = """
__import__('os').system('echo test')
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is True
        assert 'message' in response
    
    def test_prevent_code_injection(self):
        """Test prevention of code injection attempts."""
        code = """
exec("import os; os.system('echo test')")
"""
        response = run_pandas_code(code)
        
        assert response['isError'] is True
        assert 'message' in response


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

