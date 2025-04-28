# Excel-MCP Server Visualization Project

This project provides visualization capabilities for Excel data through an MCP server interface, generating interactive charts using Pyecharts.

## Features

- Generate bar, line, and pie charts from Excel data
- Customizable chart templates
- MCP server integration for remote chart generation
- Metadata handling for data formatting

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the server:
```bash
python server.py
```



## Chart Generation

Available chart types:
- Bar charts (`/generate/bar`)
- Line charts (`/generate/line`) 
- Pie charts (`/generate/pie`)

Each endpoint accepts Excel data and returns an interactive HTML chart.

## Configuration

Edit `config.py` to customize:
- Server port
- Default chart styles
- Template paths

## Dependencies

- Python 3.8+
- Pyecharts
- Flask
- Pandas
- Openpyxl