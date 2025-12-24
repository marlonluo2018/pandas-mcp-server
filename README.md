# Pandas-MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub stars](https://img.shields.io/github/stars/marlonluo2018/pandas-mcp-server?style=social)](https://github.com/marlonluo2018/pandas-mcp-server)

<div align="center">

**🚀 Powerful tool for AI-powered data analysis - Through MCP protocol, enables LLMs to safely and efficiently execute pandas code and generate visualizations**

[![GitHub stars](https://img.shields.io/github/stars/marlonluo2018/pandas-mcp-server?style=for-the-badge&logo=github&label=Star%20this%20project)](https://github.com/marlonluo2018/pandas-mcp-server/stargazers)

*If you find this project helpful, please consider giving it a ⭐️ star!*

</div>

---

A comprehensive Model Context Protocol (MCP) server that enables LLMs to execute pandas code through a standardized workflow for data analysis and visualization.

## ✨ Key Features

- 🔒 **Secure Execution Environment** - Sandboxed code execution prevents malicious operations and protects system security
- 📊 **Intelligent Data Analysis** - Automatically extracts file metadata, understands data structure, and provides intelligent analysis suggestions
- 🎨 **Interactive Visualizations** - One-click generation of various interactive charts with real-time parameter adjustment
- 🧠 **Memory Optimization** - Intelligent memory management supports large file processing with automatic data type optimization
- 🔧 **Easy Integration** - Simple configuration for seamless integration with AI assistants like Claude Desktop
- 📝 **CLI Support** - Provides command-line interface for convenient testing and development

## 🎯 MCP Server Overview

The Pandas-MCP Server is designed as a **Model Context Protocol (MCP) server** that provides LLMs with powerful data processing capabilities. MCP is a standardized protocol that allows AI models to interact with external tools and services in a secure, structured way.


## 🛠️ Installation

### Prerequisites
- Python 3.10+
- pip package manager
- Git (for cloning the repository)

### Step 1: Clone the Repository
```bash
git clone https://github.com/marlonluo2018/pandas-mcp-server.git
cd pandas-mcp-server
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables (Optional)
The server supports extensive configuration through environment variables. Copy the example configuration file:

```bash
cp .env.example .env
```

Edit the `.env` file to customize settings such as:
- Log levels and file locations
- File size limits
- Feature flags (enable/disable chart generation, code execution)
- Memory monitoring settings
- Security blacklist extensions

For detailed configuration options, see [CONFIGURATION.md](CONFIGURATION.md).

### Step 4: Verify Installation
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

### Installation with uvx (Recommended)

**uvx** is a fast Python package installer and runner that makes it easy to run Python tools without manual environment setup.

#### Install uvx
```bash
# Using pip
pip install uv

# Or using pipx (recommended for isolation)
pipx install uv
```

#### Run with uvx
```bash
# Run the MCP server directly (from local directory)
uvx --from . pandas-mcp-server

# Run the CLI tool (from local directory)
uvx --from . pandas-mcp-cli

# Run with additional arguments
uvx --from . pandas-mcp-cli metadata data.xlsx
```

#### uvx Advantages
- **No manual installation**: Automatically downloads and runs the package
- **Isolated environments**: Each run uses a clean virtual environment
- **Fast**: Uses uv's fast dependency resolver
- **Version pinning**: Easy to run specific versions

### Claude Desktop Configuration

#### Using Python (Traditional)
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

#### Using uvx (Recommended)
Add this configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "pandas-server": {
      "type": "stdio",
      "command": "uvx",
      "args": ["--from", "/path/to/pandas-mcp-server", "pandas-mcp-server"]
    }
  }
}
```

**Path Format by Operating System:**

- **Windows**: Use forward slashes (recommended) or escaped backslashes
  - `C:/Project/pandas-mcp-server` (recommended)
  - `C:\\Project\\pandas-mcp-server` (escaped backslashes)
  
- **macOS/Linux**: Use forward slashes
  - `/Users/username/projects/pandas-mcp-server`
  - `/home/username/projects/pandas-mcp-server`

**Note**: Replace `/path/to/pandas-mcp-server` with the absolute path to your pandas-mcp-server directory. The full path is required because Claude Desktop executes commands from its own working directory.

### Configuration File Location
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Verification
After configuration, restart Claude Desktop. The server should appear in the MCP tools list with four available tools:
- `read_metadata_tool` - File analysis
- `interpret_column_data` - Column value interpretation
- `run_pandas_code_tool` - Code execution  
- `generate_chartjs_tool` - Chart generation

## 🔄 Workflow

The pandas MCP server follows a structured workflow for data analysis and visualization:

### Step 1: Read File Metadata
**LLM calls `read_metadata_tool`** to understand the file structure:
- Extract file type, size, encoding, and column information
- Get data types, sample values, and statistical summaries
- Receive data quality warnings and suggested operations
- Understand the dataset structure before processing

### Step 2: Interpret Column Values (Optional)
**LLM calls `interpret_column_data`** to understand specific columns:
- Extract all unique values from important columns
- Identify patterns in categorical data
- Understand the meaning behind codes or abbreviations
- **Key Purpose**: Complement metadata by providing deep understanding of column values, which helps LLM generate more accurate and effective pandas code in the next step, especially when working with multiple CSV files

**When to Use interpret_column_data:**
- **High Value**: Categorical fields with limited unique values (Region, Status, Category)
- **High Value**: Code fields that need interpretation (StatusCode "A", "B", "C")
- **High Value**: Fields with abbreviations or cryptic values
- **Low Value**: ID fields (usually unique values with no patterns)
- **Low Value**: Email fields (typically unique identifiers)
- **Low Value**: Numeric percentage fields (already self-explanatory)
- **Conditional**: Time fields (useful for non-standard formats or categorical time)

### Step 3: Execute Pandas Operations
**LLM calls `run_pandas_code_tool`** based on metadata and column analysis:
- Formulate pandas operations using the understood file structure
- Execute data processing, filtering, aggregation, or analysis
- Receive results in DataFrame, Series, or dictionary format
- Get optimized output with memory management

### Step 4: Generate Visualizations
**LLM calls `generate_chartjs_tool`** to create interactive charts:
- Transform processed data into Chart.js compatible format
- Generate interactive HTML charts with customization controls
- Create bar, line, or pie charts based on data characteristics
- Output responsive visualizations for analysis presentation

### How `interpret_column_data` Complements `read_metadata`

The `interpret_column_data` function is designed to complement the `read_metadata_tool` by providing deeper insights into column values:

- **`read_metadata_tool`**: Focuses on file structure, data types, and statistical summaries
  - Provides high-level understanding of the dataset
  - Offers sample values and basic statistics
  - Helps LLM understand the overall data architecture

- **`interpret_column_data`**: Focuses on detailed value analysis of specific columns
  - Reveals all unique values and their frequencies
  - Helps LLM understand categorical data patterns
  - Enables more precise filtering and grouping operations
  - Particularly valuable when working with multiple CSV files where consistent value understanding across datasets is crucial

This two-step approach ensures that LLM has both structural and value-level understanding before generating pandas code, resulting in more accurate and effective data analysis operations, especially when processing multiple CSV files.

## 🚀 MCP Server Tools

The server exposes four main tools for LLM integration:

### 1. `read_metadata_tool` - File Analysis
Extract comprehensive metadata from Excel and CSV files including:
- File type, size, encoding, and structure
- Column names, data types, and sample values
- Statistical summaries (null counts, unique values, min/max/mean)
- Data quality warnings and suggested operations
- Memory-optimized processing for large files

**Purpose**: Provides LLM with a high-level understanding of the data structure and characteristics, serving as the foundation for data analysis.

**MCP Tool Usage:**
```json
{
  "tool": "read_metadata_tool",
  "args": {
    "file_path": "/path/to/sales_data.xlsx"
  }
}
```

### 2. `interpret_column_data` - Column Value Interpretation
Interpret specific columns to understand their value patterns:
- Extract all unique values with their counts from specified columns
- Support for single or multiple column interpretation
- Automatic pattern recognition for common data types
- Complete value distribution without sampling
- Support for both CSV (.csv) and Excel (.xlsx, .xls) files
- Excel worksheet selection capability

**Purpose**: Complements `read_metadata_tool` by providing deep insights into column values, enabling LLM to generate more precise filtering, grouping, and analysis operations, especially when working with multiple CSV files that require consistent value understanding across datasets.

**Best Use Cases:**
- **Most Valuable**: Categorical fields with limited unique values (Region, Status, Category)
- **Most Valuable**: Code/abbreviation fields that need interpretation (StatusCode "A", "B", "C")
- **Less Valuable**: ID fields, email fields, or numeric percentage fields
- **Context-Dependent**: Time fields (useful for non-standard formats)

#### Response Format
The function returns a structured response with the following format:
```json
{
  "columns_interpretation": [
    {
      "column_name": "Region",
      "data_type": "object",
      "total_values": 1000,
      "null_count": 5,
      "unique_count": 4,
      "unique_values_with_counts": [
        ["North", 350],
        ["South", 280],
        ["East", 220],
        ["West", 145]
      ]
    }
  ]
}
```

#### Key Features
- **Complete Value Distribution**: Returns all unique values with their exact counts
- **Sorted by Frequency**: Values are sorted in descending order of occurrence
- **Data Type Analysis**: Identifies the underlying data type (object, int64, etc.)
- **Quality Metrics**: Provides null count and total values for data quality assessment
- **Multi-column Support**: Can analyze multiple columns in a single request

**MCP Tool Usage:**
```json
{
  "tool": "interpret_column_data",
  "args": {
    "file_path": "/path/to/sales_data.csv",
    "column_names": ["Region", "Status"]
  }
}
```

**Excel File Usage (with optional sheet selection):**
```json
{
  "tool": "interpret_column_data",
  "args": {
    "file_path": "/path/to/sales_data.xlsx",
    "column_names": ["Region", "Status"],
    "sheet_name": "Q3_Sales"  // Optional: sheet name or index (default: 0)
  }
}
```

### 3. `run_pandas_code_tool` - Secure Code Execution
Execute pandas operations with:
- Security filtering against malicious code
- Memory optimization for large datasets
- Comprehensive error handling and debugging
- Support for DataFrame, Series, and dictionary results

**Purpose**: Leverages insights from both `read_metadata_tool` and `interpret_column_data` to execute precise data analysis operations, particularly valuable when processing multiple CSV files with consistent value patterns.

#### Forbidden Operations
The following operations are blocked for security reasons:
- **System Access**: `os.`, `sys.`, `subprocess.` - Prevents file system and system access
- **Code Execution**: `open()`, `exec()`, `eval()` - Blocks dynamic code execution
- **Dangerous Imports**: `import os`, `import sys` - Prevents specific harmful imports
- **Browser/DOM Access**: `document.`, `window.`, `XMLHttpRequest` - Blocks browser operations
- **JavaScript/Remote**: `fetch()`, `eval()`, `Function()` - Prevents remote code execution
- **Script Injection**: `script`, `javascript:` - Blocks script injection attempts

**Requirements:**
- Final result must be assigned to `result` variable
- Code should include necessary imports (pandas available as `pd`)
- All code goes through security filtering before execution

**MCP Tool Usage:**
```json
{
  "tool": "run_pandas_code_tool",
  "args": {
    "code": "import pandas as pd\ndf = pd.read_excel('/path/to/data.xlsx')\nresult = df.groupby('Region')['Sales'].sum()"
  }
}
```

### 4. `generate_chartjs_tool` - Interactive Visualizations
Generate interactive charts with Chart.js:
- **Bar charts** - For categorical comparisons
- **Line charts** - For trend analysis
- **Pie charts** - For proportional data
- Interactive HTML templates with customization controls

#### Chart Output
- **File Format**: All charts are generated as standalone HTML files
- **Save Location**: Charts are saved in the `./charts/` directory by default
- **File Naming**: Files are automatically named with timestamp and chart type (e.g., `bar_chart_20250710_143022.html`)
- **Accessibility**: HTML files can be opened in any web browser and shared easily

**MCP Tool Usage:**
```json
{
  "tool": "generate_chartjs_tool",
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

### CLI Interface (Testing & Development)

The CLI provides a convenient command-line interface for testing the MCP server functionality without requiring an MCP client:

#### Interactive Mode
```bash
# Using Python
python cli.py

# Using uvx
uvx pandas-mcp-cli
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
uvx pandas-mcp-cli metadata data.xlsx

# Interpret column values (useful for multiple CSV files)
python cli.py interpret data.csv --columns "Region,Status"
uvx pandas-mcp-cli interpret data.csv --columns "Region,Status"

# Execute pandas code
python cli.py execute analysis.py
uvx pandas-mcp-cli execute analysis.py

# Generate charts
python cli.py chart data.json --type bar --title "Sales Analysis"
uvx pandas-mcp-cli chart data.json --type bar --title "Sales Analysis"
```

#### Chart Output Information
When generating charts using the CLI:
- **Output Format**: Charts are saved as interactive HTML files
- **Default Location**: All charts are saved in the `./charts/` directory
- **File Naming**: Automatic naming with timestamp and chart type
- **Viewing Charts**: Open the HTML files in any web browser to view interactive visualizations
- **Sharing**: HTML files can be easily shared with others

## 🔍 Code Logic & Architecture

### Core Components

#### 1. Server Architecture (`server.py`)
- **FastMCP Integration**: Uses FastMCP framework for MCP protocol implementation
- **Logging System**: Unified logging with rotation and memory tracking
- **Tool Registration**: Exposes four main tools with proper error handling
- **Memory Monitoring**: Tracks memory usage before/after operations

#### 2. Metadata Processing (`core/metadata.py`)
**Key Logic:**
- File validation (existence, size limits)
- Encoding detection for CSV files
- Memory-optimized data processing (100-row samples)
- Comprehensive statistical analysis
- Data quality assessment and warnings

**Memory Optimization:**
- Uses `category` dtype for string columns with low cardinality
- Converts float64 to float32 for memory efficiency
- Processes only first 100 rows for metadata extraction
- Forces garbage collection after processing

#### 3. Code Execution (`core/execution.py`)
**Security Features:**
- Blacklist filtering for dangerous operations
- Sandboxed execution environment
- Output capture and error handling
- Memory monitoring for large results

**Execution Flow:**
1. Security check against BLACKLIST patterns
2. Syntax validation through compilation
3. Code execution in isolated environment
4. Result formatting and memory optimization
5. Output capture and error reporting

#### 4. Chart Generation (`core/visualization.py`)
**Architecture:**
- Template-based HTML generation
- Chart.js integration via CDN
- Interactive controls for customization
- Automatic file naming and organization

**Chart Types:**
- **Bar Charts**: Categorical data with bar width and Y-axis controls
- **Line Charts**: Trend analysis with line styling options
- **Pie Charts**: Proportional data with donut hole and percentage display

#### 5. Column Interpretation (`core/column_interpretation.py`)
**Functionality:**
- Complete value distribution analysis for specified columns
- Unique value extraction with exact counts
- Data type identification and quality metrics
- Multi-column processing in a single request
- Particularly valuable when working with multiple CSV files to ensure consistent value understanding across datasets

**Key Features:**
- Value frequency sorting (descending order)
- Null value detection and reporting
- Memory-optimized processing for large datasets
- Support for categorical and numerical data
- Enables consistent data analysis across multiple CSV files

#### 6. Chart Generators (`core/chart_generators/`)
**Base Class (`base.py`):**
- Abstract base class for all chart generators
- Template management and file I/O
- Common chart configuration

**Specific Generators:**
- `BarChartGenerator`: Bar charts with interactive controls
- `LineChartGenerator`: Line charts with tension and styling
- `PieChartGenerator`: Pie charts with legend and percentage options

### Data Flow Architecture

```
User Input → Security Check → Processing → Result → Output
    ↓              ↓            ↓         ↓         ↓
  CLI/MCP → BLACKLIST → Memory Opt → Format → Log/Display
```

### Memory Management Strategy

1. **Chunked Processing**: Large files processed in 10KB chunks
2. **Type Optimization**: Automatic dtype conversion (float64→float32, object→category)
3. **Limited Sampling**: Only first 100 rows processed for metadata
4. **Garbage Collection**: Forced cleanup after major operations
5. **Memory Monitoring**: PSutil integration for tracking usage

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
│   ├── column_interpretation.py   # Column value analysis
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
├── csv_metadata_format.md   # CSV metadata documentation
└── test_*.py               # Test files
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

## 📊 Chart Generation Details

### HTML Chart Files
All charts generated by the Pandas-MCP Server are saved as standalone HTML files with the following characteristics:

#### File Structure
- **Self-contained**: Each HTML file includes all necessary CSS and JavaScript
- **Interactive**: Charts include controls for customization (zoom, filter, etc.)
- **Responsive**: Charts adapt to different screen sizes
- **No Dependencies**: HTML files work offline without internet connection

#### Save Location
- **Default Directory**: `./charts/` (created automatically if it doesn't exist)
- **Configuration**: Can be changed in `core/config.py` by modifying `CHARTS_DIR`
- **File Naming Pattern**: `{chart_type}_chart_{timestamp}.html`
  - Example: `bar_chart_20250710_143022.html`
  - Example: `line_chart_20250710_143547.html`

#### Usage
1. **Viewing**: Simply double-click the HTML file to open it in a web browser
2. **Sharing**: Send the HTML file to others - no additional software needed
3. **Embedding**: HTML files can be embedded in web pages or iframes
4. **Printing**: Use browser's print function to save charts as PDF

### Template System
Charts are generated using HTML templates with:
- Chart.js integration via CDN
- Interactive controls for customization
- Responsive design with mobile support
- Real-time parameter adjustment

### Chart Types

#### Bar Charts
- Interactive controls for bar width and Y-axis scaling
- Responsive design with zoom capabilities
- Data labels and tooltips
- Multiple dataset support

#### Line Charts
- Multiple line series support
- Adjustable line tension and styling
- Point size and style customization
- Stepped line options

#### Pie Charts
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

## 📄 Additional Documentation

- **CSV Metadata Format**: See `csv_metadata_format.md` for detailed CSV processing documentation
- **API Documentation**: Check our [API documentation](docs/api.md) for detailed usage instructions

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Getting Help
- **Report Issues**: Submit an [issue](https://github.com/marlonluo2018/pandas-mcp-server/issues) on GitHub
- **Discussions**: Join our [GitHub Discussions](https://github.com/marlonluo2018/pandas-mcp-server/discussions)

### Frequently Asked Questions
Check our [FAQ](docs/faq.md) page for answers to common questions.

### Contact Information
- Email: [marlonluo2018@foxmail.com](mailto:marlonluo2018@foxmail.com)

---

## 🌟 Show Your Support

If you find this project useful, please consider giving it a ⭐️ star on GitHub! Your support helps us:

- Increase project visibility
- Attract more users
- Motivate continued development
- Build a stronger community

[![GitHub stars](https://img.shields.io/github/stars/marlonluo2018/pandas-mcp-server?style=for-the-badge&logo=github&label=Star%20this%20project)](https://github.com/marlonluo2018/pandas-mcp-server/stargazers)

---

## 📊 Project Statistics

[![GitHub issues](https://img.shields.io/github/issues/marlonluo2018/pandas-mcp-server)](https://github.com/marlonluo2018/pandas-mcp-server/issues)
[![GitHub forks](https://img.shields.io/github/forks/marlonluo2018/pandas-mcp-server)](https://github.com/marlonluo2018/pandas-mcp-server/network)
[![GitHub stars](https://img.shields.io/github/stars/marlonluo2018/pandas-mcp-server)](https://github.com/marlonluo2018/pandas-mcp-server/stargazers)

---

<div align="center">

**Thank you for your support! Please give us a ⭐️ Star if you find this project helpful!**

[🔝 Back to top](#pandas-mcp-server)

</div>
