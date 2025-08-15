# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Pandas-MCP Server** - a Model Context Protocol (MCP) server that enables LLMs to execute pandas code through a standardized workflow for data analysis and visualization. The server provides three main tools: file metadata extraction, secure pandas code execution, and interactive chart generation.

## Development Commands

### Installation and Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Test CLI interface
python cli.py

# Test MCP server
python server.py
```

### Testing
```bash
# Test metadata extraction
python test_metadata.py

# Test pandas code execution  
python test_execution.py

# Test chart generation
python test_generate_barchart.py
python test_generate_pyecharts.py

# Run all tests with pytest
pytest
```

### CLI Interface
```bash
# Interactive mode (recommended for testing)
python cli.py

# Command-line mode
python cli.py metadata data.xlsx
python cli.py execute analysis.py
python cli.py chart data.json --type bar --title "Sales Analysis"
```

## Architecture Overview

### Core Components

1. **Server Layer** (`server.py`)
   - FastMCP integration for MCP protocol
   - Three exposed tools: `read_metadata_tool`, `run_pandas_code_tool`, `generate_chartjs_tool`
   - Unified logging system with rotation
   - Memory monitoring with psutil

2. **Metadata Processing** (`core/metadata.py`)
   - File validation and encoding detection
   - Memory-optimized processing (100-row samples)
   - Comprehensive statistical analysis
   - Automatic dtype optimization (float64→float32, object→category)

3. **Code Execution** (`core/execution.py`)
   - Security filtering with BLACKLIST patterns
   - Sandboxed execution environment
   - Result formatting and memory optimization
   - Comprehensive error handling

4. **Chart Generation** (`core/visualization.py` + `core/chart_generators/`)
   - Template-based HTML generation using Chart.js
   - Three chart types: bar, line, pie
   - Interactive controls and responsive design
   - Automatic file naming and organization

### Security Architecture

- **BLACKLIST filtering**: Prevents dangerous operations (os.*, sys.*, subprocess, etc.)
- **Sandboxed execution**: Code runs in isolated environment
- **Memory limits**: 100MB file size limit with monitoring
- **Input validation**: All file paths and data validated

### Data Flow

```
User Input → Security Check → Memory Optimization → Processing → Result → Output
    ↓              ↓              ↓              ↓         ↓         ↓
  CLI/MCP → BLACKLIST → dtype conversion → pandas → Format → Log/Display
```

## Configuration

### Core Settings (`core/config.py`)
- `MAX_FILE_SIZE`: 100MB file size limit
- `BLACKLIST`: Security restrictions for code execution
- `CHARTS_DIR`: Directory for generated charts
- Logging: 5MB rotation with 3 backup files

### Dependencies
- `pandas>=2.0.0` - Data manipulation
- `fastmcp>=1.0.0` - MCP server framework
- `chardet>=5.0.0` - Character encoding detection
- `psutil>=5.9.0` - System monitoring
- `pytest>=7.0.0` - Testing framework

## Memory Management Strategy

1. **Chunked Processing**: Large files processed in 10KB chunks
2. **Type Optimization**: Automatic dtype conversion for memory efficiency
3. **Limited Sampling**: Only first 100 rows for metadata extraction
4. **Garbage Collection**: Forced cleanup after major operations
5. **Memory Monitoring**: PSutil integration with detailed logging

## MCP Tool Interface

The server exposes three MCP tools with specific data structures:

### 1. read_metadata_tool
Input: `file_path` (string)
Output: Structured metadata with file info, column analysis, and statistics

### 2. run_pandas_code_tool  
Input: `code` (string containing pandas operations)
Output: Formatted results or error information

### 3. generate_chartjs_tool
Input: `data` (structured dict with columns), `chart_types`, `title`
Output: Interactive HTML chart with file path

## Testing Approach

- **Unit tests**: Individual component testing (pytest framework)
- **Integration tests**: End-to-end workflow testing
- **Manual testing**: CLI interface for interactive validation
- **Memory testing**: Monitor memory usage during operations

## Development Notes

- All chart templates use Chart.js via CDN for interactive visualizations
- Logging is centralized with rotation to prevent disk space issues
- Memory optimization is critical - always consider dtype conversion and sampling
- Security is paramount - all code execution goes through BLACKLIST filtering
- The CLI interface provides excellent testing capabilities without MCP client setup