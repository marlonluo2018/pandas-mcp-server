# Pandas MCP Server

This repository contains a server implementation using the Model Context Protocol (MCP) with functionalities to handle CSV files, execute Pandas code, and generate interactive charts (bar charts and pie charts).

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

### bar_chart_to_html

- **Description**: Generates an interactive HTML bar chart using Chart.js template.
- **Parameters**:
  - `categories`: List of category names for x-axis
  - `values`: List of numeric values for y-axis
  - `title`: Chart title (default: "Interactive Chart")
- **Returns**:
  - A dictionary containing the file path and status information
- **Example**:
```python
bar_chart_to_html(
    categories=['Electronics', 'Clothing', 'Home Goods'],
    values=[120000, 85000, 95000],
    title="Q1 Sales by Product Category"
)
```

### pie_chart_to_html

- **Description**: Generates an interactive HTML pie chart using Chart.js template.
- **Parameters**:
  - `labels`: List of label names for each pie slice
  - `values`: List of numeric values for each slice
  - `title`: Chart title (default: "Interactive Pie Chart")
- **Returns**:
  - A dictionary containing the file path and status information
- **Example**:
```python
pie_chart_to_html(
    labels=['Electronics', 'Clothing', 'Home Goods'],
    values=[120000, 85000, 95000],
    title="Q1 Sales Distribution"
)
```

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

## Workflow

1. Load and inspect your CSV file:
   - User prompt: "Load the CSV file at data/sample.csv and show me the column structure"
   - This will call `load_csv_tool` with the file path

2. Execute Pandas operations on the loaded data:
   - User prompt: "Group the data by category and calculate the sum for each group"
   - This will call `run_pandas_code` with the appropriate Pandas operation
