import sys
from io import StringIO
import traceback
import pandas as pd
from .config import BLACKLIST
import logging

logger = logging.getLogger(__name__)

def run_pandas_code(code: str) -> dict:
    """Execute pandas code with smart suggestions and security checks.
    
    Requirements:
        - Must contain full import and file loading logic using the provided file_path
        - Must assign final result to 'result' variable
        - Code must use the provided file_path to load data
    
    Returns:
        dict: Either the result or error information
        
    Example:
        >>> run_pandas_code('''
        ... import pandas as pd
        ... df = pd.read_csv(file_path)
        ... result = df.sum()
        ... ''', '/path/to/data.csv')
        {
            "result": {
                "type": "series",
                "data": {"A": 3, "B": 7},
                "dtype": "int64"
            }
        }
    """
    # Security checks
    for forbidden in BLACKLIST:
        if forbidden in code:
            return {
                "error": {
                    "type": "SECURITY_VIOLATION",
                    "message": f"Forbidden operation detected: {forbidden}",
                    "solution": "Remove restricted operations from your code"
                }
            }

    # Prepare execution environment with memory optimizations
    local_vars = {
        'pd': pd,
        'read_csv_chunked': lambda path: pd.read_csv(path, chunksize=10000),
        'read_excel_chunked': lambda path: pd.read_excel(path, chunksize=10000)
    }
    stdout_capture = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_capture

    try:
        # First check for syntax errors
        try:
            compile(code, '<string>', 'exec')
        except Exception as e:  # Catch all compilation errors
            logger.error(f"Code compilation failed: {str(e)}")
            return {
                "content": [],
                "error": {
                    "isError": True,
                    "message": f"Code error: {str(e)}",
                    "traceback": traceback.format_exc(),
                    "output": stdout_capture.getvalue()
                }
            }

        # Execute with memory monitoring
        try:
            exec(code, {}, local_vars)
        except Exception as e:
            logger.error(f"Code execution failed: {str(e)}")
            return {
                "content": [],
                "error": {
                    "isError": True,
                    "message": str(e),
                    "traceback": traceback.format_exc(),
                    "output": stdout_capture.getvalue()
                }
            }
        
        # Clear intermediate variables
        for var in list(local_vars.keys()):
            if var not in ('result', 'pd'):
                del local_vars[var]
                
        result = local_vars.get('result', None)
        logger.debug(f"Result type: {type(result)}")
        logger.debug(f"Result value: {result}")

        if result is None:
            return {
                "content": [],
                "isError": True,
                "message": "No 'result' variable found in code",
                "output": stdout_capture.getvalue()
            }

        # Handle memory optimization for large DataFrames/Series
        if isinstance(result, (pd.DataFrame, pd.Series)):
            if hasattr(result, 'memory_usage'):
                mem_usage = result.memory_usage(deep=True).sum()
                if mem_usage > 1e8:  # >100MB
                    result = result.head(100)
        
        # Format result
        if isinstance(result, (pd.DataFrame, pd.Series)):
            content = result.to_dict()
        elif isinstance(result, dict):
            content = result
        else:
            content = str(result)
        
        logger.debug(f"Final content: {content}")
        
        return {
            "content": [content] if content is not None else [],
            "isError": False
        }

    except Exception as e:
        logger.error(f"Execution failed: {str(e)}")
        return {
            "content": [],
            "isError": True,
            "message": str(e),
            "traceback": traceback.format_exc(),
            "output": stdout_capture.getvalue()
        }
    finally:
        sys.stdout = old_stdout