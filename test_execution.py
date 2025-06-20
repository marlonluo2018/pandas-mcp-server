import pytest
from core.execution import run_pandas_code
import pandas as pd

def test_run_pandas_code_with_dataframe():
    """Test successful execution with DataFrame result"""
    code = """
import pandas as pd
df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
result = df
"""
    response = run_pandas_code(code)
    assert not response['isError']
    assert len(response['content']) == 1
    assert isinstance(response['content'][0], dict)
    assert 'A' in response['content'][0]

def test_run_pandas_code_with_dict():
    """Test successful execution with dict result"""
    code = """
result = {'original_rows': 100, 'filtered_rows': 50}
"""
    response = run_pandas_code(code)
    assert not response['isError']
    assert len(response['content']) == 1
    assert response['content'][0]['original_rows'] == 100
    assert response['content'][0]['filtered_rows'] == 50

def test_run_pandas_code_error():
    """Test error case"""
    # Test with guaranteed syntax error
    code = "import pandas as pd\nx = 1 + "  # Missing operand
    response = run_pandas_code(code)
    assert response['error']['isError']
    assert 'message' in response['error']
    assert 'traceback' in response['error']

    # Test with clear runtime error
    code = """
import pandas as pd
df = pd.DataFrame({'A': [1, 2]})
result = df['nonexistent_column']  # Will raise KeyError
"""
    response = run_pandas_code(code)
    assert response['error']['isError']
    assert 'message' in response['error']
    assert 'traceback' in response['error']
    assert 'traceback' in response['error']

def test_run_pandas_code_no_result():
    """Test case where no result variable is set"""
    code = """
x = 1 + 1
"""
    response = run_pandas_code(code)
    assert response['isError']
    assert "No 'result' variable found" in response['message']