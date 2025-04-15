from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
from chardet import detect
import traceback
from io import StringIO
import sys

mcp = FastMCP("PandasAgent")

# Constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
BLACKLIST = ['os.', 'sys.', 'subprocess.', 'open(', 'exec(', 'eval(', 'import os', 'import sys']

@mcp.tool()
def load_csv_tool(file_path: str) -> dict:
    """
    Load CSV file and return metadata in MCP-compatible format
    
    Args:
        file_path: Absolute path to CSV
        
    Returns:
        dict: Structured metadata including:
        - columns: List with name/type/sample for each column
        - file_info: Size and encoding details
        - status: SUCCESS/ERROR indicator
        
    Example:
    >>> load_csv_tool("/path/to/file.csv")
    {
        "status": "SUCCESS",
        "columns": [
            {"name": "id", "type": "int64", "sample": [1, 2]},
            {"name": "name", "type": "object", "sample": ["Alice", "Bob"]}
        ],
        "file_info": {
            "size": "45.3KB",
            "encoding": "utf-8"
        }
    }
    """
    try:
        # Validate file existence and size
        if not os.path.exists(file_path):
            return {"status": "ERROR", "error": "FILE_NOT_FOUND", "path": file_path}
            
        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            return {
                "status": "ERROR",
                "error": "FILE_TOO_LARGE",
                "max_size": f"{MAX_FILE_SIZE/1024/1024}MB",
                "actual_size": f"{file_size/1024/1024:.1f}MB"
            }

        # Detect encoding and delimiter
        with open(file_path, 'rb') as f:
            rawdata = f.read(50000)
            enc = detect(rawdata)['encoding'] or 'utf-8'
            
        with open(file_path, 'r', encoding=enc) as f:
            first_line = f.readline()
            delimiter = ',' if ',' in first_line else '\t' if '\t' in first_line else ';'

        # Try using dask for large files
        if file_size > MAX_FILE_SIZE:
            return {
                "status": "ERROR",
                "error": "FILE_TOO_LARGE",
                "max_size": f"{MAX_FILE_SIZE/1024/1024}MB",
                "actual_size": f"{file_size/1024/1024:.1f}MB"
            }
        else:
            df = pd.read_csv(file_path, encoding=enc, delimiter=delimiter, nrows=100)

        # Format response
        return {
            "status": "SUCCESS",
            "columns": [
                {
                    "name": col,
                    "type": str(df[col].dtype),
                    "sample": df[col].dropna().iloc[:2].tolist()
                }
                for col in df.columns
            ],
            "file_info": {
                "size": f"{file_size/1024:.1f}KB",
                "encoding": enc,
                "delimiter": delimiter
            }
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "error_type": type(e).__name__,
            "message": str(e),
            "solution": [
                "Check if the file is being used by another program",
                "Try saving the file as UTF-8 encoded CSV",
                "Contact the administrator to check MCP file access permissions"
            ],
            "traceback": traceback.format_exc()
        }

@mcp.tool()
def run_pandas_code(code: str) -> dict:
    """
    Execute pandas code with smart suggestions and security checks
    
    Requirements:
    - Must contain full import and file loading logic
    - Must assign final result to 'result' variable
    
    Returns:
        dict: Either the result or error information
        
    Example:
    >>> run_pandas_code('''
    ... import pandas as pd
    ... df = pd.DataFrame({'A': [1,2], 'B': [3,4]})
    ... result = df.sum()
    ... ''')
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


if __name__ == "__main__":
    mcp.run()
