import sys
from io import StringIO
import traceback
import pandas as pd
from config import BLACKLIST

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
        # Execute with memory monitoring
        exec(code, {}, local_vars)
        
        # Clear intermediate variables
        for var in list(local_vars.keys()):
            if var not in ('result', 'pd'):
                del local_vars[var]
                
        result = local_vars.get('result', None)

        if result is None:
            return {
                "output": stdout_capture.getvalue(),
                "warning": "No 'result' variable found in code"
            }

        # Format different result types with memory efficiency
        if isinstance(result, (pd.DataFrame, pd.Series)):
            response = {
                "result": {
                    "type": "dataframe" if isinstance(result, pd.DataFrame) else "series",
                    "shape": result.shape,
                    "dtypes": str(result.dtypes),
                    # Only sample data to reduce memory
                    "data": result.head(100).to_dict() if isinstance(result, pd.DataFrame)
                          else result.head(100).to_dict()
                }
            }
            # Clear full result if not needed
            if hasattr(result, 'memory_usage'):
                mem_usage = result.memory_usage(deep=True).sum()
                if mem_usage > 1e8:  # >100MB
                    result = result.head(100)
        else:
            response = {"result": str(result)}

        return response
        
    except Exception as e:
        # Generate specific suggestions based on error
        error_msg = str(e)
        suggestions = []

        if "No such file or directory" in error_msg:
            suggestions.append("Use raw strings for paths: r'path\\to\\file.csv'")
        if "could not convert string to float" in error_msg:
            suggestions.append("Try: pd.to_numeric(df['col'], errors='coerce')")
        if "AttributeError" in error_msg and "str" in error_msg:
            suggestions.append("Try: df['col'].astype(str).str.strip()")

        return {
            "error": {
                "type": type(e).__name__,
                "message": error_msg,
                "traceback": traceback.format_exc(),
                "output": stdout_capture.getvalue(),
                "suggestions": suggestions if suggestions else None
            }
        }
    finally:
        sys.stdout = old_stdout