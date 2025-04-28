import logging
import traceback
from config import mcp
from metadata import read_metadata
from execution import run_pandas_code
from visualization import generate_chartjs

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@mcp.tool()
def read_metadata_tool(file_path: str) -> dict:
    """Read file metadata (Excel or CSV) and return in MCP-compatible format.
    
    Args:
        file_path: Absolute path to data file
        
    Returns:
        dict: Structured metadata including:
            For Excel:
                - file_info: {type: "excel", sheet_count, sheet_names}
                - data: {sheets: [{sheet_name, rows, columns}]}
            For CSV:
                - file_info: {type: "csv", encoding, delimiter}
                - data: {rows, columns}
            Common:
                - status: SUCCESS/ERROR
                - columns contain:
                    - name, type, examples
                    - stats: null_count, unique_count
                    - warnings, suggested_operations
    
    Example:
        >>> read_metadata_wrapper("data/sample.xlsx")
        {
            "status": "SUCCESS",
            "file_info": {
                "type": "excel",
                "sheet_count": 3,
                "sheet_names": ["Sheet1", "Sheet2", "Sheet3"]
            },
            "data": {
                "sheets": [
                    {
                        "name": "Sheet1",
                        "rows": 100,
                        "columns": [
                            {
                                "name": "Date",
                                "type": "datetime",
                                "examples": ["2023-01-01", "2023-01-02"],
                                "stats": {
                                    "null_count": 0,
                                    "unique_count": 100
                                }
                            }
                        ]
                    }
                ]
            }
        }
    """
    return read_metadata(file_path)

@mcp.tool()
def run_pandas_code_tool(code: str) -> dict:
    """Execute pandas code with smart suggestions and security checks.
    
    Args:
        code: Python code string containing pandas operations
        
    Returns:
        dict: Either the result or error information
        
    Example:
        >>> run_pandas_code_wrapper('''
        ... import pandas as pd
        ... df = pd.read_csv(file_path)
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
    return run_pandas_code(code)

@mcp.tool()
def generate_chartjs_tool(
    data: dict,
    chart_types: list = None,
    title: str = "Data Visualization",
    request_params: dict = None,
    **kwargs
) -> dict:
    """Generate interactive Chart.js visualizations from structured data.
    
    Args:
        data: Structured data in MCP format with required structure:
            {
                "columns": [
                    {
                        "name": str,        # Column name
                        "type": str,        # Data type ("string", "number", etc)
                        "examples": list    # Sample values from column
                    },
                    ...
                ]
            }
        chart_types: List of supported chart types to generate (first is used).
            Supported types: ["pie", "bar", "line"]
        title: Chart title string
        request_params: Additional visualization parameters (optional)
        **kwargs: Additional chart options (optional)
        
    Returns:
        dict: Result with structure:
            {
                "status": "SUCCESS"|"ERROR",
                "chart_html": str,         # Generated HTML content
                "chart_type": str,         # Type of chart generated
                "html_path": str,          # Path to saved HTML file
                "message": str,             # Error message if status=ERROR
                "traceback": str            # Error traceback if status=ERROR
            }
        
    Example:
        >>> generate_chartjs_tool(
        ...     data={
        ...         "columns": [
        ...             {
        ...                 "name": "Month",
        ...                 "type": "string",
        ...                 "examples": ["Jan", "Feb", "Mar"]
        ...             },
        ...             {
        ...                 "name": "Revenue",
        ...                 "type": "number",
        ...                 "examples": [150, 240, 350]
        ...             }
        ...         ]
        ...     },
        ...     chart_types=["bar"],
        ...     title="Monthly Revenue"
        ... )
        {
            "status": "SUCCESS",
            "chart_html": "<div>...</div>",
            "chart_type": "bar",
            "html_path": "/path/to/chart.html"
        }
    """
    return generate_chartjs(data, chart_types, title, request_params, **kwargs)

def main():
    try:
        logger.debug("Starting stdio MCP server...")
        mcp.run()
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}")
        logger.debug(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
