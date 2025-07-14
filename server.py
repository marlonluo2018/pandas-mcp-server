import logging
import traceback
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from core.config import mcp
from core.metadata import read_metadata
from core.execution import run_pandas_code
from core.visualization import generate_chartjs

def setup_logging():
    """Configure logging with all components writing to a single file"""
    # Create logs directory
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Single log file path
    log_file = os.path.join(log_dir, 'mcp_server.log')
    
    # Common formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Configure single rotating file handler
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.DEBUG,
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
    
    return {'server': log_file}

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
        logger.error(f"Unexpected error in read_metadata_tool: {str(e)}")
        logger.debug(traceback.format_exc())
        return {
            "status": "ERROR",
            "error_type": "TOOL_EXECUTION_ERROR",
            "message": str(e)
        }

@mcp.tool()
def run_pandas_code_tool(code: str) -> dict:
    """Execute pandas code with smart suggestions and security checks.
    
    Args:
        code: Python code string containing pandas operations
        
    Returns:
        dict: Either the result or error information
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
        logger.error(f"Server failed to start: {str(e)}")
        logger.debug(traceback.format_exc())
        raise

if __name__ == "__main__":
    main()
