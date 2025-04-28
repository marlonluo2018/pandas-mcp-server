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

    # Prepare execution environment
    local_vars = {'pd': pd}
    stdout_capture = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_capture

    try:
        exec(code, {}, local_vars)
        result = local_vars.get('result', None)

        if result is None:
            return {
                "output": stdout_capture.getvalue(),
                "warning": "No 'result' variable found in code"
            }

        # Format different result types appropriately
        if isinstance(result, (pd.DataFrame, pd.Series)):
            response = {
                "result": {
                    "type": "dataframe" if isinstance(result, pd.DataFrame) else "series",
                    "shape": result.shape,
                    "dtypes": str(result.dtypes),
                    "data": result.head().to_dict() if isinstance(result, pd.DataFrame) else result.to_dict()
                }
            }
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