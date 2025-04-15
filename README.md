# Pandas MCP Server

This repository contains a server implementation using the Model Context Protocol (MCP) with functionalities to handle CSV files and execute Pandas code.

## Requirements

- Python 3.11 or higher
- Install required packages: `pip install -r requirements.txt`

## Functions

### load_csv_tool

- **Description**: Loads a CSV file and returns its column structure and sample data.
- **Parameters**:
  - `file_path`: Path to the CSV file.
- **Returns**:
  - A dictionary containing the columns and sample data from the CSV file.
- **Notes**:
  - Detects file encoding and delimiter automatically.
  - Limits file size to 100MB to prevent excessive memory usage.

### run_pandas_code

- **Description**: Executes Pandas code provided as a string.
- **Parameters**:
  - `file_path`: Path to the CSV file to be loaded into a DataFrame.
  - `code`: String containing the Pandas code to execute.
- **Returns**:
  - A dictionary containing the result of the executed code and any variables created during execution.
- **Security Notes**:
  - Prevents execution of blacklisted operations such as `os.`, `sys.`, `subprocess.`, `open(`, `exec(`, `eval(`, `import os`, `import sys`.
  - Provides detailed error messages and suggestions to help users resolve issues.

## Usage

1. Configure your MCP client with the following settings:
```json
{
  "mcpServers": {
    "pandas": {
      "name": "pandas",
      "type": "stdio",
      "description": "run pandas code",
      "isActive": true,
      "command": "python",
      "args": [
        "${workspaceFolder}/server.py"
      ]
    }
  }
}
```
2. Use the configured MCP client to interact with the server and utilize the provided tools.


