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

## Usage

### 1. MCP Client Configuration
Configure your MCP client (e.g. Cursor, Claude, or VS Code with Cline plugin) with this JSON configuration:

```json
{
  "mcpServers": {
    "pandas-server": {
      "name": "pandas",
      "type": "stdio",
      "description": "Run pandas code via MCP protocol",
      "isActive": true,
      "command": "python",
      "args": [
        "${workspaceFolder}/server.py"
      ]
    }
  }
}

2. Use an MCP client to interact with the server and utilize the provided tools.

## Testing

- Run the tests: `python test.py`
- This will execute the test cases for both `load_csv_tool` and `run_pandas_code`.

## Contributing

Feel free to contribute by submitting issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
