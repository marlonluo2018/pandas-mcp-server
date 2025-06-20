from mcp.server.fastmcp import FastMCP
import os

# Configuration
CHARTS_DIR = os.path.join(os.path.dirname(__file__), 'charts')
os.makedirs(CHARTS_DIR, exist_ok=True)

# Constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
BLACKLIST = [
    'os.', 'sys.', 'subprocess.', 'open(', 'exec(', 'eval(',
    'import os', 'import sys', 'document.', 'window.', 'XMLHttpRequest',
    'fetch(', 'eval(', 'Function(', 'script', 'javascript:'
]

# MCP Server Initialization
mcp = FastMCP("Excel-MCP-Server")