# Pandas MCP Server Configuration Guide

## Overview

The Pandas MCP Server supports extensive configuration through environment variables, allowing you to customize behavior without modifying code.

## Environment Variables

### Directory Configuration

#### `PANDAS_MCP_CHARTS_DIR`
- **Description**: Directory where generated chart files are saved
- **Default**: `./core/charts`
- **Example**: `PANDAS_MCP_CHARTS_DIR=/path/to/charts`

### File Size Limits

#### `PANDAS_MCP_MAX_FILE_SIZE`
- **Description**: Maximum file size in bytes that can be processed
- **Default**: `104857600` (100MB)
- **Example**: `PANDAS_MCP_MAX_FILE_SIZE=52428800` (50MB)

### Logging Configuration

#### `PANDAS_MCP_LOG_LEVEL`
- **Description**: Logging verbosity level
- **Default**: `INFO`
- **Valid Values**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Example**: `PANDAS_MCP_LOG_LEVEL=DEBUG`

#### `PANDAS_MCP_LOG_FILE`
- **Description**: Path to the log file
- **Default**: `./logs/mcp_server.log`
- **Example**: `PANDAS_MCP_LOG_FILE=/var/log/pandas-mcp-server.log`

#### `PANDAS_MCP_LOG_MAX_BYTES`
- **Description**: Maximum size of a log file before rotation (in bytes)
- **Default**: `5242880` (5MB)
- **Example**: `PANDAS_MCP_LOG_MAX_BYTES=10485760` (10MB)

#### `PANDAS_MCP_LOG_BACKUP_COUNT`
- **Description**: Number of backup log files to keep after rotation
- **Default**: `3`
- **Example**: `PANDAS_MCP_LOG_BACKUP_COUNT=5`

### Performance Settings

#### `PANDAS_MCP_ENABLE_MEMORY_MONITORING`
- **Description**: Enable memory usage monitoring and logging
- **Default**: `true`
- **Valid Values**: `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off`
- **Example**: `PANDAS_MCP_ENABLE_MEMORY_MONITORING=true`

#### `PANDAS_MCP_MEMORY_WARNING_THRESHOLD`
- **Description**: Memory usage threshold in MB that triggers warnings
- **Default**: `500` (500MB)
- **Example**: `PANDAS_MCP_MEMORY_WARNING_THRESHOLD=1000` (1GB)

### Feature Flags

#### `PANDAS_MCP_ENABLE_CHART_GENERATION`
- **Description**: Enable/disable chart generation functionality
- **Default**: `true`
- **Valid Values**: `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off`
- **Example**: `PANDAS_MCP_ENABLE_CHART_GENERATION=true`

#### `PANDAS_MCP_ENABLE_CODE_EXECUTION`
- **Description**: Enable/disable pandas code execution functionality
- **Default**: `true`
- **Valid Values**: `true`, `false`, `1`, `0`, `yes`, `no`, `on`, `off`
- **Example**: `PANDAS_MCP_ENABLE_CODE_EXECUTION=true`

### Security Configuration

#### `PANDAS_MCP_BLACKLIST`
- **Description**: Additional forbidden operations (comma-separated)
- **Default**: Built-in security blacklist
- **Example**: `PANDAS_MCP_BLACKLIST=eval,exec,subprocess`

## Setting Environment Variables

### Method 1: Using a `.env` file

1. Copy the example configuration:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your desired values:
```bash
# Example .env file
PANDAS_MCP_LOG_LEVEL=DEBUG
PANDAS_MCP_MAX_FILE_SIZE=52428800
PANDAS_MCP_ENABLE_MEMORY_MONITORING=true
```

3. Load the environment variables before running the server:
```bash
# On Linux/Mac
source .env

# On Windows (PowerShell)
Get-Content .env | ForEach-Object { $var = $_.Split('='); [Environment]::SetEnvironmentVariable($var[0], $var[1]) }
```

### Method 2: Setting directly in the shell

#### Linux/Mac (bash/zsh)
```bash
export PANDAS_MCP_LOG_LEVEL=DEBUG
export PANDAS_MCP_MAX_FILE_SIZE=52428800
python -m server
```

#### Windows (PowerShell)
```powershell
$env:PANDAS_MCP_LOG_LEVEL="DEBUG"
$env:PANDAS_MCP_MAX_FILE_SIZE=52428800
python -m server
```

#### Windows (Command Prompt)
```cmd
set PANDAS_MCP_LOG_LEVEL=DEBUG
set PANDAS_MCP_MAX_FILE_SIZE=52428800
python -m server
```

### Method 3: Using python-dotenv (recommended for production)

1. Install python-dotenv:
```bash
pip install python-dotenv
```

2. Create a `.env` file with your configuration

3. Load it in your application:
```python
from dotenv import load_dotenv
load_dotenv()  # This loads variables from .env file
```

## Viewing Current Configuration

You can view the current configuration by importing the config module and calling `print_config()`:

```python
from core.config import print_config
print_config()
```

This will display all configuration values:
```
============================================================
Pandas MCP Server Configuration
============================================================
CHARTS_DIR: ./core/charts
MAX_FILE_SIZE: 100.00 MB
LOG_LEVEL: INFO
LOG_FILE: ./logs/mcp_server.log
LOG_MAX_BYTES: 5.00 MB
LOG_BACKUP_COUNT: 3
ENABLE_MEMORY_MONITORING: True
MEMORY_WARNING_THRESHOLD: 500 MB
ENABLE_CHART_GENERATION: True
ENABLE_CODE_EXECUTION: True
BLACKLIST items: 14
============================================================
```

## Security Considerations

### Feature Flags in Production

When deploying to production, consider disabling certain features for security:

```bash
# Disable code execution in production
PANDAS_MCP_ENABLE_CODE_EXECUTION=false

# Disable chart generation if not needed
PANDAS_MCP_ENABLE_CHART_GENERATION=false
```

### Blacklist Configuration

The built-in blacklist includes common security risks. You can extend it:

```bash
PANDAS_MCP_BLACKLIST=eval,exec,subprocess,os.system,sys.exit
```

### File Size Limits

Set appropriate file size limits based on your server's resources:

```bash
# For servers with limited memory
PANDAS_MCP_MAX_FILE_SIZE=52428800  # 50MB

# For servers with ample memory
PANDAS_MCP_MAX_FILE_SIZE=524288000  # 500MB
```

## Troubleshooting

### Configuration Not Applied

If environment variables don't seem to be applied:

1. Verify the variable is set:
```bash
echo $PANDAS_MCP_LOG_LEVEL  # Linux/Mac
echo %PANDAS_MCP_LOG_LEVEL%  # Windows CMD
$env:PANDAS_MCP_LOG_LEVEL   # Windows PowerShell
```

2. Check for typos in variable names
3. Ensure the `.env` file is loaded before starting the server

### Logging Issues

If logs aren't appearing:

1. Check the log file path exists and is writable:
```bash
ls -la ./logs/mcp_server.log  # Linux/Mac
dir logs\mcp_server.log       # Windows
```

2. Verify log level is set correctly:
```bash
PANDAS_MCP_LOG_LEVEL=DEBUG
```

3. Check file permissions:
```bash
chmod 755 ./logs  # Linux/Mac
```

### Feature Disabled Errors

If you see "Feature disabled" errors:

1. Check the feature flag is enabled:
```bash
PANDAS_MCP_ENABLE_CHART_GENERATION=true
PANDAS_MCP_ENABLE_CODE_EXECUTION=true
```

2. Restart the server after changing environment variables

## Best Practices

1. **Use `.env` files**: Keep configuration in version-controlled `.env.example` and local `.env` files
2. **Document custom values**: Comment your `.env` file to explain why values were changed
3. **Test in development**: Test configuration changes in development before production
4. **Monitor logs**: Use appropriate log levels (INFO for production, DEBUG for development)
5. **Set memory limits**: Configure memory thresholds based on available resources
6. **Disable unused features**: Turn off features you don't need for better security
7. **Regular review**: Periodically review and update configuration settings

## Example Configurations

### Development Environment
```bash
PANDAS_MCP_LOG_LEVEL=DEBUG
PANDAS_MCP_ENABLE_MEMORY_MONITORING=true
PANDAS_MCP_MEMORY_WARNING_THRESHOLD=500
PANDAS_MCP_ENABLE_CHART_GENERATION=true
PANDAS_MCP_ENABLE_CODE_EXECUTION=true
```

### Production Environment
```bash
PANDAS_MCP_LOG_LEVEL=INFO
PANDAS_MCP_LOG_FILE=/var/log/pandas-mcp-server/mcp_server.log
PANDAS_MCP_LOG_MAX_BYTES=10485760
PANDAS_MCP_LOG_BACKUP_COUNT=10
PANDAS_MCP_ENABLE_MEMORY_MONITORING=true
PANDAS_MCP_MEMORY_WARNING_THRESHOLD=1000
PANDAS_MCP_MAX_FILE_SIZE=104857600
PANDAS_MCP_ENABLE_CHART_GENERATION=true
PANDAS_MCP_ENABLE_CODE_EXECUTION=false
```

### High-Security Environment
```bash
PANDAS_MCP_LOG_LEVEL=WARNING
PANDAS_MCP_LOG_FILE=/var/log/pandas-mcp-server/mcp_server.log
PANDAS_MCP_ENABLE_MEMORY_MONITORING=true
PANDAS_MCP_MEMORY_WARNING_THRESHOLD=500
PANDAS_MCP_MAX_FILE_SIZE=52428800
PANDAS_MCP_ENABLE_CHART_GENERATION=false
PANDAS_MCP_ENABLE_CODE_EXECUTION=false
PANDAS_MCP_BLACKLIST=eval,exec,subprocess,os.system,sys.exit,compile
```
