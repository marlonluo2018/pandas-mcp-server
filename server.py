import logging
import traceback
import os
from logging.handlers import RotatingFileHandler
from core.config import mcp
from core.metadata import read_metadata
from core.execution import run_pandas_code
from core.visualization import generate_chartjs

# Configure logging to both console and file
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'mcp_server.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            log_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        ),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
try:
    logger.info(f"Logging configured. Log file: {log_file}")
except PermissionError as e:
    logger.error(f"Failed to create log file: {e}")

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
        >>> read_metadata("data/sample.xlsx")
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
        >>> run_pandas_code('''
        ... import pandas as pd
        ... # For Windows paths, use raw strings to avoid escape issues:
        ... df = pd.read_csv(r'C:\\path\\to\\file.csv')
        ...
        ... # Convert value_counts() to dict for cleaner output:
        ... counts = df['column'].value_counts().to_dict()
        ...
        ... # Always assign to 'result' variable for proper return:
        ... result = df.describe()
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
    request_params: dict = None
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
    return generate_chartjs(data, chart_types, title, request_params)

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
