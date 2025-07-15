# Pandas-MCP Server

A comprehensive Model Context Protocol (MCP) server that enables LLMs to execute pandas code through a standardized workflow for data analysis and visualization.

## 🎯 Overview

The Pandas-MCP Server provides a complete data processing pipeline with three core capabilities:

1. **Metadata Reading** - Extract structured metadata from Excel/CSV files
2. **Pandas Execution** - Process and analyze data with security checks
3. **Chart Generation** - Create interactive visualizations with Chart.js

## 🚀 Core Features

### MCP Server Tools
The server exposes three main tools for LLM integration:

#### 1. `read_metadata` - File Analysis
Extract comprehensive metadata from Excel and CSV files including:
- File type, size, encoding, and structure
- Column names, data types, and sample values
- Statistical summaries (null counts, unique values, min/max/mean)
- Data quality warnings and suggested operations
- Memory-optimized processing for large files

#### 2. `run_pandas_code` - Secure Code Execution
Execute pandas operations with:
- Security filtering against malicious code
- Memory optimization for large datasets
- Comprehensive error handling and debugging
- Support for DataFrame, Series, and dictionary results

#### 3. `generate_chartjs` - Interactive Visualizations
Generate interactive charts with Chart.js:
- **Bar charts** - For categorical comparisons
- **Line charts** - For trend analysis
- **Pie charts** - For proportional data
- Interactive HTML templates with customization controls

### User-Friendly CLI Interface
The `cli.py` provides both interactive and command-line modes:

#### Interactive Mode
```bash
python cli.py
```
Launches a guided menu system with:
- Step-by-step workflow guidance
- Automatic input validation
- Clear error messages
- Support for file paths with spaces

#### Command-Line Mode
```bash
# Read metadata
python cli.py metadata data.xlsx

# Execute pandas code
python cli.py execute analysis.py

# Generate charts
python cli.py chart data.json --type bar --title "Sales Analysis"
```

## 📁 Project Structure

```
pandas-mcp-server/
├── cli.py                    # Command-line interface
├── server.py                 # MCP server implementation
├── requirements.txt          # Python dependencies
├── core/                     # Core functionality
│   ├── config.py            # Configuration and constants
│   ├── data_types.py        # Data type utilities
│   ├── metadata.py          # File metadata extraction
│   ├── execution.py         # Pandas code execution
│   ├── visualization.py     # Chart generation orchestration
│   └── chart_generators/    # Chart-specific implementations
│       ├── __init__.py
│       ├── base.py          # Base chart generator
│       ├── bar.py           # Bar chart generator
│       ├── line.py          # Line chart generator
│       └── pie.py           # Pie chart generator
│       └── templates/       # HTML templates for charts
├── charts/                  # Generated chart files
├── logs/                    # Application logs
└── tests/                   # Test files
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Dependencies
- **pandas>=2.0.0** - Data manipulation and analysis
- **fastmcp>=1.0.0** - MCP server framework
- **chardet>=5.0.0** - Character encoding detection
- **psutil** - System monitoring for memory optimization

## 🚀 Usage

### Starting the MCP Server
```bash
python server.py
```

The server will start and expose the three main tools to connected LLMs.

### Using the CLI

#### Interactive Mode
```bash
python cli.py
```

#### Direct Commands
```bash
# Read file metadata
python cli.py metadata /path/to/data.xlsx

# Execute pandas script
python cli.py execute /path/to/analysis.py

# Generate visualization
python cli.py chart /path/to/data.json --type line --title "Revenue Trends"
```

### MCP Tool Usage Examples

#### Reading File Metadata
```python
{
  "tool": "read_metadata",
  "args": {
    "file_path": "/path/to/sales_data.xlsx"
  }
}
```

#### Executing Pandas Code
```python
{
  "tool": "run_pandas_code",
  "args": {
    "code": """
import pandas as pd
df = pd.read_excel('/path/to/sales_data.xlsx')
result = df.groupby('Region')['Sales'].sum()
"""
  }
}
```

#### Generating Charts
```python
{
  "tool": "generate_chartjs",
  "args": {
    "data": {
      "columns": [
        {
          "name": "Region",
          "type": "string",
          "examples": ["North", "South", "East", "West"]
        },
        {
          "name": "Sales",
          "type": "number",
          "examples": [15000, 12000, 18000, 9000]
        }
      ]
    },
    "chart_types": ["bar"],
    "title": "Sales by Region"
  }
}
```

## 🔧 Configuration

### Core Configuration (`core/config.py`)
- **MAX_FILE_SIZE**: 100MB file size limit
- **BLACKLIST**: Security restrictions for code execution
- **CHARTS_DIR**: Directory for generated charts
- **Logging**: Comprehensive logging with rotation

### Security Features
- Code execution sandboxing
- Blacklisted operations (file system, network, eval)
- Memory usage monitoring
- Input validation and sanitization

## 📊 Chart Types

### Bar Charts
- Interactive controls for bar width and Y-axis scaling
- Responsive design with zoom capabilities
- Data labels and tooltips

### Line Charts
- Multiple line series support
- Adjustable line tension and styling
- Point size and style customization
- Stepped line options

### Pie Charts
- Interactive donut hole adjustment
- Percentage/value toggle display
- Legend positioning and styling
- Border width and color controls

## 🧪 Testing

### Running Tests
```bash
# Test metadata extraction
python test_metadata.py

# Test pandas code execution
python test_execution.py

# Test chart generation
python test_generate_barchart.py

# Test all chart types
python test_generate_pyecharts.py
```

### Test Data Requirements
- Excel files (.xlsx) with multiple sheets
- CSV files with various encodings
- JSON files with structured data for chart generation

## 📈 Performance Optimization

### Memory Management
- Chunked processing for large files
- Automatic garbage collection
- Memory usage logging
- Dataset size limits

### File Processing
- Optimized dtype inference
- Category encoding for string columns
- Float32 precision for numeric data
- Streaming CSV reading

## 🔍 Logging

### Log Structure
- **mcp_server.log**: Main application log
- **memory_usage**: Memory consumption tracking
- **metadata**: File processing details

### Log Levels
- DEBUG: Detailed processing information
- INFO: General operation status
- WARNING: Non-critical issues
- ERROR: Processing failures

## 🐛 Troubleshooting

### Common Issues

#### File Not Found
- Verify file path is absolute
- Check file permissions
- Ensure file exists before processing

#### Memory Issues
- Reduce file size or use chunked processing
- Monitor memory usage in logs
- Consider data sampling for large datasets

#### Chart Generation Errors
- Verify data structure matches expected format
- Check for required columns (string + numeric)
- Ensure Chart.js CDN accessibility

### Debug Mode
Enable debug logging by setting environment variable:
```bash
export LOG_LEVEL=DEBUG
python server.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the troubleshooting section
- Review log files in the `logs/` directory
- Open an issue on GitHub with reproduction steps