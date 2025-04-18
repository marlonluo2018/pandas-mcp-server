# Pandas MCP Server

This repository contains a server implementation using the Model Context Protocol (MCP) with functionalities to handle CSV files, execute Pandas code, and generate interactive charts (bar charts and pie charts).

## Requirements

- Python 3.11 or higher
- Install required packages: `pip install -r requirements.txt`

## Functions

### read_metadata

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
```json
{
    "categories": ["Electronics", "Clothing", "Home Goods"],
    "values": [120000, 85000, 95000],
    "title": "Q1 Sales by Product Category"
}
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
```json
{
    "labels": ["Electronics", "Clothing", "Home Goods"],
    "values": [120000, 85000, 95000],
    "title": "Q1 Sales Distribution"
}
```

### line_chart_to_html

- **Description**: Generates an interactive HTML line chart using Chart.js template.
- **Parameters**:
  - `labels`: List of label names for x-axis
    - `datasets`: List of datasets, each containing:
      - `label`: Name of the dataset
      - `data`: List of numeric values
  - `title`: Chart title (default: "Interactive Line Chart")
- **Returns**:
  - A dictionary containing the file path and status information
- **Example**:
```json
{
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [
        {
            "label": "Sales",
            "data": [12000, 15000, 18000]
        },
        {
            "label": "Expenses",
            "data": [8000, 9000, 10000]
        }
    ],
    "title": "Monthly Performance"
}
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

1. Read metadata of your CSV file:
   - User prompt: "Read metadata of data/sample.csv and show me the column structure"
   - This will call `read_metadata` with the file path

2. Execute Pandas operations on the loaded data:
   - User prompt: "Group the data by category and calculate the sum for each group"
   - This will call `run_pandas_code` with the appropriate Pandas operation

3. Visualize the results using charts:
   - User prompt: "Create a bar chart showing sales by category"
   - This will call `bar_chart_to_html` with the grouped data
   - Example response:
```json
{
    "status": "SUCCESS",
    "filepath": "/absolute/path/to/chart_1713443200.html"
}
```
