# Pandas-MCP Server

A comprehensive Model Context Protocol (MCP) server that enables LLMs to execute pandas code through a standardized workflow for data analysis and visualization.

## 🎯 MCP Server Overview

The Pandas-MCP Server is designed as a **Model Context Protocol (MCP) server** that provides LLMs with powerful data processing capabilities. MCP is a standardized protocol that allows AI models to interact with external tools and services in a secure, structured way.

### What is MCP?
Model Context Protocol (MCP) is an open standard that enables secure, structured communication between AI models and external tools. It provides:
- **Standardized tool interfaces** for consistent AI interactions
- **Security boundaries** to prevent unauthorized operations
- **Structured data exchange** with type safety
- **Extensible architecture** for custom tool development

### Why Use This MCP Server?
- **Secure Data Processing**: Execute pandas operations with built-in security checks
- **Structured Metadata**: Extract comprehensive file information in standardized format
- **Interactive Visualizations**: Generate Chart.js visualizations directly from data
- **Memory Optimized**: Handle large datasets efficiently with chunked processing
- **LLM-Ready**: Designed specifically for AI model integration

## �️ Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Git (for cloning the repository)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/pandas-mcp-server.git
cd pandas-mcp-server
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
# Test the CLI interface
python cli.py

# Or test the MCP server directly
python server.py
```

### Dependencies
- **pandas>=2.0.0** - Data manipulation and analysis
- **fastmcp>=1.0.0** - MCP server framework
- **chardet>=5.0.0** - Character encoding detection
- **psutil** - System monitoring for memory optimization

### Claude Desktop Configuration
Add this configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "pandas-server": {
      "type": "stdio",
      "command": "python",
      "args": ["/path/to/your/pandas-mcp-server/server.py"]
    }
  }
}
```

**Note**: Replace `/path/to/your/pandas-mcp-server/server.py` with the actual path where you cloned the repository.

**Example paths:**
- Windows: `"C:\\Users\\YourName\\pandas-mcp-server\\server.py"`
- macOS/Linux: `"/home/username/pandas-mcp-server/server.py"`
```

### Configuration File Location
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Verification
After configuration, restart Claude Desktop. The server should appear in the MCP tools list with three available tools:
- `read_metadata` - File analysis
- `run_pandas_code` - Code execution  
- `generate_chartjs` - Chart generation

## 🚀 MCP Server Tools

The server exposes three main tools for LLM integration:

### 1. `read_metadata` - File Analysis
Extract comprehensive metadata from Excel and CSV files including:
- File type, size, encoding, and structure
- Column names, data types, and sample values
- Statistical summaries (null counts, unique values, min/max/mean)
- Data quality warnings and suggested operations
- Memory-optimized processing for large files

**MCP Tool Usage:**
```json
{
  "tool": "read_metadata",
  "args": {
    "file_path": "/path/to/sales_data.xlsx"
  }
}
```

### 2. `run_pandas_code` - Secure Code Execution
Execute pandas operations with:
- Security filtering against malicious code
- Memory optimization for large datasets
- Comprehensive error handling and debugging
- Support for DataFrame, Series, and dictionary results

**MCP Tool Usage:**
```json
{
  "tool": "run_pandas_code",
  "args": {
    "code": "import pandas as pd\ndf = pd.read_excel('/path/to/data.xlsx')\nresult = df.groupby('Region')['Sales'].sum()"
  }
}
```

### 3. `generate_chartjs` - Interactive Visualizations
Generate interactive charts with Chart.js:
- **Bar charts** - For categorical comparisons
- **Line charts** - For trend analysis
- **Pie charts** - For proportional data
- Interactive HTML templates with customization controls

**MCP Tool Usage:**
```json
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

## 🚀 Usage

### Starting the MCP Server
```bash
python server.py
```

The server will start and expose the three main tools to connected LLMs via the MCP protocol.

### CLI Interface (Testing & Development)

The `cli.py` provides a convenient command-line interface for testing the MCP server functionality without requiring an MCP client:

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
├── server.py                 # MCP server implementation
├── cli.py                    # CLI interface for testing
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

#### MCP Connection Issues
- Verify server path in Claude Desktop configuration
- Check Python environment and dependencies
- Ensure server.py is executable
- Review MCP server logs for connection errors

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
