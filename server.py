import logging
import traceback
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from core.config import mcp, LOG_LEVEL, LOG_FILE, LOG_MAX_BYTES, LOG_BACKUP_COUNT
from core.metadata import read_metadata
from core.execution import run_pandas_code
from core.visualization import generate_chartjs
from core.column_interpretation import interpret_column_values
from core.error_handling import ErrorType, handle_exception

def setup_logging():
    """Configure logging with all components writing to a single file"""
    # Create logs directory from config
    log_dir = os.path.dirname(LOG_FILE)
    os.makedirs(log_dir, exist_ok=True)
    
    # Common formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Configure single rotating file handler using config values
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=LOG_MAX_BYTES,
        backupCount=LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Configure root logger using config log level
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        handlers=[
            file_handler,
            logging.StreamHandler()
        ]
    )
    
    # Configure memory logger to use same handler
    memory_logger = logging.getLogger('memory_usage')
    memory_logger.addHandler(file_handler)
    memory_logger.addHandler(logging.StreamHandler())
    
    # Configure metadata logger to use same handler
    metadata_logger = logging.getLogger('metadata')
    metadata_logger.addHandler(file_handler)
    metadata_logger.addHandler(logging.StreamHandler())
    
    return {'server': LOG_FILE}

logger = logging.getLogger(__name__)

def init_logging():
    """Initialize logging system and verify setup"""
    try:
        log_files = setup_logging()
        
        logger.info(f"Logging configured with single log file: {list(log_files.values())[0]}")
        
        # Log file permissions
        if os.path.exists(list(log_files.values())[0]):
            permissions = oct(os.stat(list(log_files.values())[0]).st_mode)[-3:]
            logger.info(f"Log file created with permissions: {permissions}")
            
        return True
    except PermissionError as e:
        logger.error(f"Failed to create/access log files: {e}")
        logger.error(f"Please check directory permissions for: {os.path.dirname(list(log_files.values())[0])}")
        return False

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
    """
    try:
        logger.info(f"Starting metadata read for file: {file_path}")
        import psutil
        process = psutil.Process()
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        memory_logger = logging.getLogger('memory_usage')
        memory_logger.debug(f"Memory usage before read_metadata: {mem_before:.1f}MB")
        
        result = read_metadata(file_path)
        
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_logger.debug(f"Memory usage after read_metadata: {mem_after:.1f}MB")
        memory_logger.debug(f"Memory change: {mem_after - mem_before:.1f}MB")
        
        if result['status'] == 'ERROR':
            logger.error(f"Metadata read failed: {result.get('message', 'Unknown error')}")
            if 'traceback' in result:
                logger.debug(f"Error traceback:\n{result['traceback']}")
        return result
    except Exception as e:
        return handle_exception(
            e,
            ErrorType.TOOL_EXECUTION_ERROR,
            "read_metadata_tool failed"
        )

@mcp.tool()
def interpret_column_data(
    file_path: str,
    column_names: list,
    sheet_name: str = 0
) -> dict:
    """Interpret column values and return their unique values.
    
    This tool is most valuable for categorical fields with limited unique values,
    code fields that need interpretation, and fields with abbreviations or cryptic values.
    
    Best use cases:
    - HIGH VALUE: Categorical fields (Region, Status, Category)
    - HIGH VALUE: Code fields (StatusCode "A", "B", "C")
    - HIGH VALUE: Fields with abbreviations or cryptic values
    - LOW VALUE: ID fields (usually unique values with no patterns)
    - LOW VALUE: Email fields (typically unique identifiers)
    - LOW VALUE: Numeric percentage fields (already self-explanatory)
    - CONDITIONAL: Time fields (useful for non-standard formats or categorical time)
    
    Supported file types:
    - CSV (.csv) files
    - Excel (.xlsx, .xls) files (reads first sheet by default)
    
    Args:
        file_path: Absolute path to data file
        column_names: List of column names to interpret
        sheet_name: Sheet name or index to read from Excel files (default: 0, first sheet)
        
    Returns:
        dict: Structured interpretation including:
            - status: SUCCESS/ERROR
            - file_info: Basic file information
            - columns_interpretation: List of column interpretations with:
                - column_name: Name of the column
                - unique_values_with_counts: List of (value, count) tuples
                - unique_count: Total number of unique values
                - total_values: Total number of values in the column
                - null_count: Number of null values
                - data_type: Type of data in the column
    """
    try:
        logger.info(f"Starting column value analysis for file: {file_path}")
        import psutil
        process = psutil.Process()
        mem_before = process.memory_info().rss / 1024 / 1024  # MB
        memory_logger = logging.getLogger('memory_usage')
        memory_logger.debug(f"Memory usage before interpret_column_values: {mem_before:.1f}MB")
        
        result = interpret_column_values(file_path, column_names, sheet_name)
        
        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        memory_logger.debug(f"Memory usage after interpret_column_values: {mem_after:.1f}MB")
        memory_logger.debug(f"Memory change: {mem_after - mem_before:.1f}MB")
        
        if result['status'] == 'ERROR':
            logger.error(f"Column value analysis failed: {result.get('message', 'Unknown error')}")
        
        return result
    except Exception as e:
        return handle_exception(
            e,
            ErrorType.TOOL_EXECUTION_ERROR,
            "interpret_column_data failed"
        )

@mcp.tool()
def run_pandas_code_tool(code: str) -> dict:
    """Execute pandas code with smart suggestions and security checks.
    
    Args:
        code: Python code string containing pandas operations
        
    Returns:
        dict: Either the result or error information
        
    Forbidden Operations:
        The following operations are blocked for security reasons:
        - 'os.', 'sys.', 'subprocess.' - System access operations
        - 'open(', 'exec(', 'eval(' - Code execution functions
        - 'import os', 'import sys' - Specific dangerous imports
        - 'document.', 'window.', 'XMLHttpRequest' - Browser/DOM access
        - 'fetch(', 'eval(', 'Function(' - JavaScript/remote operations
        - 'script', 'javascript:' - Script injection attempts
        
    Requirements:
        - Must assign final result to 'result' variable
        - Code should contain necessary imports (pandas available as 'pd')
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
                        "name": str,      # Column name
                        "type": str,       # "string" or "number"
                        "examples": list   # Array of values
                    },
                    ...                   # Additional columns
                ]
            }
            Example:
            {
                "columns": [
                    {
                        "name": "Category",
                        "type": "string",
                        "examples": ["A", "B", "C"]
                    },
                    {
                        "name": "Value",
                        "type": "number",
                        "examples": [10, 20, 30]
                    }
                ]
            }
        chart_types: List of supported chart types to generate (first is used)
        title: Chart title string
        request_params: Additional visualization parameters (optional)
        
    Returns:
        dict: Result with structure:
            {
                "status": "SUCCESS"|"ERROR",
                "chart_html": str,         # Generated HTML content
                "chart_type": str,         # Type of chart generated
                "html_path": str          # Path to saved HTML file
            }
    """
    return generate_chartjs(data, chart_types, title, request_params)

def main():
    try:
        if not init_logging():
            raise RuntimeError("Failed to initialize logging")
            
        logger.debug("Starting stdio MCP server...")
        mcp.run()
    except Exception as e:
        logger.error(f"Server failed to start: {handle_exception(e, ErrorType.INTERNAL_ERROR, 'Server startup failed')['message']}")
        logger.debug(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
