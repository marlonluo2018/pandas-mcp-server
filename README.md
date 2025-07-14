# Pandas-MCP Server

A Model Context Protocol (MCP) server that enables LLMs to execute pandas code through a standardized workflow:

1. **Metadata Reading** - Understand data structure
2. **Pandas Execution** - Process and analyze data
3. **Chart Generation** - Visualize results (optional)

## Core Features

### Standard Workflow Tools
1. **read_metadata** - Extract structured metadata from Excel/CSV files
   ```python
   {
     "tool": "read_metadata",
     "args": {
       "file_path": "/path/to/data.xlsx" 
     }
   }
   ```

2. **run_pandas_code** - Execute pandas operations with smart suggestions
   ```python
   {
     "tool": "run_pandas_code",
     "args": {
       "code": "df.groupby('category').sum()"
     }
   }
   ```

3. **generate_chart** - Create visualizations (optional)
   ```python
   {
     "tool": "generate_chart",
     "args": {
       "data": {...},
       "chart_types": ["bar"]
     }
   }
   ```

## User-Friendly CLI Interface

The `cli.py` provides an intuitive menu-driven interface that guides users through the workflow without needing to remember commands:

```bash
python cli.py
```

This launches an interactive menu:
```
Excel Data Processing Tool
------------------------

Main Menu:
1. Read file metadata
2. Execute pandas code 
3. Generate chart
4. Exit

Enter your choice (1-4):
```

### Key Benefits:
- No need to remember commands - guided step-by-step
- Automatic input validation
- Clear error messages
- Handles file paths with spaces automatically

For advanced users, command-line mode is still available:
```bash
# Direct command execution
python cli.py metadata data.csv
python cli.py execute analysis.py
python cli.py chart results.json --type bar
```

## Installation

```bash
pip install -r requirements.txt
```

## Server Usage

Start the MCP server:
```bash
python server.py
```

## Configuration

Edit `core/config.py` to customize:
- Workflow steps
- Memory limits
- Logging settings

## Dependencies

- pandas>=2.0.0
- fastmcp>=1.0.0  
- chardet>=5.0.0