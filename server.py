from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
from chardet import detect
import traceback
from io import StringIO
import sys
import seaborn as sns
import time
from textwrap import wrap
import json


mcp = FastMCP("PandasAgent")

# Constants
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
BLACKLIST = ['os.', 'sys.', 'subprocess.', 'open(', 'exec(', 'eval(', 'import os', 'import sys']

@mcp.tool()
def load_csv_tool(file_path: str) -> dict:
    """Load CSV file and return metadata in MCP-compatible format.
    
    Args:
        file_path: Absolute path to CSV
        
    Returns:
        dict: Structured metadata including:
            - columns: List with name/type/sample for each column
            - file_info: Size and encoding details
            - status: SUCCESS/ERROR indicator
        
    Example:
        >>> load_csv_tool("/path/to/file.csv")
        {
            "status": "SUCCESS",
            "columns": [
                {"name": "id", "type": "int64", "sample": [1, 2]},
                {"name": "name", "type": "object", "sample": ["Alice", "Bob"]}
            ],
            "file_info": {
                "size": "45.3KB",
                "encoding": "utf-8"
            }
        }
    """
    try:
        # Validate file existence and size
        if not os.path.exists(file_path):
            return {"status": "ERROR", "error": "FILE_NOT_FOUND", "path": file_path}

        file_size = os.path.getsize(file_path)
        if file_size > MAX_FILE_SIZE:
            return {
                "status": "ERROR",
                "error": "FILE_TOO_LARGE",
                "max_size": f"{MAX_FILE_SIZE / 1024 / 1024}MB",
                "actual_size": f"{file_size / 1024 / 1024:.1f}MB"
            }

        # Detect encoding and delimiter
        with open(file_path, 'rb') as f:
            rawdata = f.read(50000)
            enc = detect(rawdata)['encoding'] or 'utf-8'

        with open(file_path, 'r', encoding=enc) as f:
            first_line = f.readline()
            delimiter = ',' if ',' in first_line else '\t' if '\t' in first_line else ';'

        # Try using dask for large files
        if file_size > MAX_FILE_SIZE:
            return {
                "status": "ERROR",
                "error": "FILE_TOO_LARGE",
                "max_size": f"{MAX_FILE_SIZE / 1024 / 1024}MB",
                "actual_size": f"{file_size / 1024 / 1024:.1f}MB"
            }
        else:
            df = pd.read_csv(file_path, encoding=enc, delimiter=delimiter, nrows=100)

        # Format response
        return {
            "status": "SUCCESS",
            "columns": [
                {
                    "name": col,
                    "type": str(df[col].dtype),
                    "sample": df[col].dropna().iloc[:2].tolist()
                }
                for col in df.columns
            ],
            "file_info": {
                "size": f"{file_size / 1024:.1f}KB",
                "encoding": enc,
                "delimiter": delimiter
            }
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "error_type": type(e).__name__,
            "message": str(e),
            "solution": [
                "Check if the file is being used by another program",
                "Try saving the file as UTF-8 encoded CSV",
                "Contact the administrator to check MCP file access permissions"
            ],
            "traceback": traceback.format_exc()
        }


@mcp.tool()
def run_pandas_code(code: str, file_path: str) -> dict:
    """Execute pandas code with smart suggestions and security checks.
    
    Requirements:
        - Must contain full import and file loading logic using the provided file_path
        - Must assign final result to 'result' variable
        - Code must use the provided file_path to load data
    
    Returns:
        dict: Either the result or error information
        
    Example:
        >>> run_pandas_code('''
        ... import pandas as pd
        ... df = pd.read_csv(file_path)
        ... result = df.sum()
        ... ''', '/path/to/data.csv')
        {
            "result": {
                "type": "series",
                "data": {"A": 3, "B": 7},
                "dtype": "int64"
            }
        }
    """
    # Validate file
    if not os.path.exists(file_path):
        return {
            "error": {
                "type": "FILE_ERROR",
                "message": f"File not found: {file_path}",
                "solution": "Check the file path and try again"
            }
        }

    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        return {
            "error": {
                "type": "FILE_ERROR",
                "message": f"File too large: {file_size / 1024 / 1024:.1f}MB (max {MAX_FILE_SIZE / 1024 / 1024}MB)",
                "solution": "Use a smaller file or increase MAX_FILE_SIZE"
            }
        }

    # Security checks
    for forbidden in BLACKLIST:
        if forbidden in code:
            return {
                "error": {
                    "type": "SECURITY_VIOLATION",
                    "message": f"Forbidden operation detected: {forbidden}",
                    "solution": "Remove restricted operations from your code"
                }
            }

    # Verify code uses the provided file_path
    if f"'{file_path}'" not in code and f'"{file_path}"' not in code:
        return {
            "error": {
                "type": "CODE_VALIDATION",
                "message": "Code must use the provided file_path to load data",
                "solution": f"Add a file loading statement using '{file_path}'"
            }
        }

    # Prepare execution environment
    local_vars = {'pd': pd}
    stdout_capture = StringIO()
    old_stdout = sys.stdout
    sys.stdout = stdout_capture

    try:
        exec(code, {}, local_vars)
        result = local_vars.get('result', None)

        if result is None:
            return {
                "output": stdout_capture.getvalue(),
                "warning": "No 'result' variable found in code"
            }

        # Format different result types appropriately
        if isinstance(result, (pd.DataFrame, pd.Series)):
            response = {
                "result": {
                    "type": "dataframe" if isinstance(result, pd.DataFrame) else "series",
                    "shape": result.shape,
                    "dtypes": str(result.dtypes),
                    "data": result.head().to_dict() if isinstance(result, pd.DataFrame) else result.to_dict()
                }
            }
        else:
            response = {"result": str(result)}

        return response
        
    except Exception as e:
        # Generate specific suggestions based on error
        error_msg = str(e)
        suggestions = []

        if "No such file or directory" in error_msg:
            suggestions.append("Use raw strings for paths: r'path\\to\\file.csv'")
        if "could not convert string to float" in error_msg:
            suggestions.append("Try: pd.to_numeric(df['col'], errors='coerce')")
        if "AttributeError" in error_msg and "str" in error_msg:
            suggestions.append("Try: df['col'].astype(str).str.strip()")

        return {
            "error": {
                "type": type(e).__name__,
                "message": error_msg,
                "traceback": traceback.format_exc(),
                "output": stdout_capture.getvalue(),
                "suggestions": suggestions if suggestions else None
            }
        }
    finally:
        sys.stdout = old_stdout



@mcp.tool()
def bar_chart_to_html(
    categories: list,
    values: list,
    title: str = "Interactive Chart",
   
) -> dict:
    """Generate interactive HTML bar chart using Chart.js template.
    
    Args:
        categories: List of category names for x-axis
        values: List of numeric values for y-axis
        title: Chart title (default: "Interactive Chart")
        x_label: Label for X-axis (default: "Categories")
        y_label: Label for Y-axis (default: "Values")
        
    Returns:
        dict: Contains file path and status information
        
    Example:
        >>> bar_chart_to_html(
        ...     categories=['Electronics', 'Clothing', 'Home Goods', 'Sports Equipment'],
        ...     values=[120000, 85000, 95000, 60000],
        ...     title="Q1 Sales by Product Category"
        ... )
        {
            "status": "SUCCESS",
            "filepath": "/absolute/path/to/plotXXXXXX.html",
        }
    """
    # Validate input lengths
    if len(categories) != len(values):
        return {
            "status": "ERROR",
            "error": "MISMATCHED_LENGTHS",
            "message": f"Categories ({len(categories)}) and values ({len(values)}) must be same length"
        }

    # Read template file
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./templates/barchart_template.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "TEMPLATE_READ_ERROR",
            "message": str(e)
        }

    # Prepare data for Chart.js
    all_categories = categories
    all_values = values
    colors = [
        "#4e73df", "#1cc88a", "#36b9cc", "#f6c23e",
        "#e74a3b", "#858796", "#f8f9fc", "#5a5c69",
        "#6610f2", "#6f42c1", "#e83e8c", "#d63384",
        "#fd7e14", "#ffc107", "#28a745", "#20c997",
        "#17a2b8", "#007bff", "#6c757d", "#343a40",
        "#dc3545", "#ff6b6b", "#4ecdc4", "#1a535c"
    ][:len(all_categories)]

    # Inject data into template
    template = template.replace(
        'labels: ["Electronics", "Clothing", "Home Goods", "Sports Equipment"]',
        f'labels: {json.dumps(all_categories)}'
    ).replace(
        'data: [120000, 85000, 95000, 60000]',
        f'data: {json.dumps(all_values)}'
    ).replace(
        'backgroundColor: ["#4e73df", "#1cc88a", "#36b9cc", "#f6c23e"]',
        f'backgroundColor: {json.dumps(colors)}'
    ).replace(
        'Sales by Category (2023)',
        title
    ).replace(
        'legend: { position: \'top\' },',
        ''
    )

    # Save to plot directory as HTML
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    timestamp = str(int(time.time()))
    filename = f"chart_{timestamp}.html"
    filepath = os.path.join(charts_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "FILE_WRITE_ERROR",
            "message": str(e)
        }

    return {
        "status": "SUCCESS",
        "filepath": os.path.abspath(filepath)
    }


@mcp.tool()
def pie_chart_to_html(
    labels: list,
    values: list,
    title: str = "Interactive Pie Chart"
) -> dict:
    """Generate interactive HTML pie chart using Chart.js template.
    
    Args:
        labels: List of label names for each pie slice
        values: List of numeric values for each slice
        title: Chart title (default: "Interactive Pie Chart")
        
    Returns:
        dict: Contains file path and status information
        
    Example:
        >>> pie_chart_to_html(
        ...     labels=['Electronics', 'Clothing', 'Home Goods'],
        ...     values=[120000, 85000, 95000],
        ...     title="Q1 Sales Distribution"
        ... )
        {
            "status": "SUCCESS",
            "filepath": "/absolute/path/to/plotXXXXXX.html",
        }
    """
    # Validate input lengths
    if len(labels) != len(values):
        return {
            "status": "ERROR",
            "error": "MISMATCHED_LENGTHS",
            "message": f"Labels ({len(labels)}) and values ({len(values)}) must be same length"
        }

    # Read template file
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./templates/piechart_template.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "TEMPLATE_READ_ERROR",
            "message": str(e)
        }

    # Prepare data for Chart.js
    colors = [
        "#4e73df", "#1cc88a", "#36b9cc", "#f6c23e",
        "#e74a3b", "#858796", "#f8f9fc", "#5a5c69",
        "#6610f2", "#6f42c1", "#e83e8c", "#d63384",
        "#fd7e14", "#ffc107", "#28a745", "#20c997",
        "#17a2b8", "#007bff", "#6c757d", "#343a40",
        "#dc3545", "#ff6b6b", "#4ecdc4", "#1a535c"
    ][:len(labels)]

    # Inject data into template
    template = template.replace(
        'labels: ["Apple", "Samsung", "Huawei", "Xiaomi", "Others"]',
        f'labels: {json.dumps(labels)}'
    ).replace(
        'data: [45, 25, 12, 8, 10]',
        f'data: {json.dumps(values)}'
    ).replace(
        'backgroundColor: ["#4e73df", "#1cc88a", "#36b9cc", "#f6c23e", "#e74a3b"]',
        f'backgroundColor: {json.dumps(colors)}'
    ).replace(
        'Global Smartphone Market Share (2023)',
        title
    )

    # Save to plot directory as HTML
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    timestamp = str(int(time.time()))
    filename = f"chart_{timestamp}.html"
    filepath = os.path.join(charts_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "FILE_WRITE_ERROR",
            "message": str(e)
        }

    return {
        "status": "SUCCESS",
        "filepath": os.path.abspath(filepath)
    }

@mcp.tool()
def line_chart_to_html(
    labels: list,
    datasets: list,
    title: str = "Interactive Line Chart"
) -> dict:
    """Generate interactive HTML line chart using Chart.js template.
    
    Args:
        labels: List of label names for x-axis
        datasets: List of datasets, each containing:
            - label: Name of the dataset
            - data: List of numeric values (3 dimensions: [x, y, z])
        title: Chart title (default: "Interactive Line Chart")
        
    Returns:
        dict: Contains file path and status information
        
    Example:
        >>> line_chart_to_html(
        ...     labels=['Jan', 'Feb', 'Mar'],
        ...     datasets=[
        ...         {'label': 'Sales', 'data': [[100, 200, 300], [150, 250, 350], [200, 300, 400]]},
        ...         {'label': 'Expenses', 'data': [[50, 100, 150], [75, 125, 175], [100, 150, 200]]}
        ...     ],
        ...     title="Monthly Performance"
        ... )
        {
            "status": "SUCCESS",
            "filepath": "/absolute/path/to/plotXXXXXX.html",
        }
    """
    # Validate input
    if not all(len(d['data']) == len(labels) for d in datasets):
        return {
            "status": "ERROR",
            "error": "MISMATCHED_LENGTHS",
            "message": "All datasets must have same length as labels"
        }

    # Read template file
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "./templates/linechart_template.html")
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "TEMPLATE_READ_ERROR",
            "message": str(e)
        }

    # Prepare data for Chart.js
    chart_data = {
        "labels": labels,
        "datasets": []
    }
    
    # Create datasets using main labels
    for dataset in datasets:
            chart_data['datasets'].append({
                "label": dataset['label'],
                "data": dataset['data'],
                "borderColor": '#4e73df',  # Default color
                "backgroundColor": '#4e73df',
            "borderWidth": 2,
            "pointRadius": 5,
            "tension": 0,
            "fill": False
        })

    # Inject data into template
    template = template.replace(
        'labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]',
        f'labels: {json.dumps(labels)}'
    ).replace(
        'datasets: [\n' +
        '                {\n' +
        '                    label: "Electronics",\n' +
        '                    data: [6500, 5900, 8000, 8100, 8600, 8250, 9500, 10500, 12000, 11500, 13000, 15000],\n' +
        '                    borderColor: "#4e73df",\n' +
        '                    backgroundColor: "#4e73df",\n' +
        '                    borderWidth: 2,\n' +
        '                    pointRadius: 5,\n' +
        '                    tension: 0,\n' +
        '                    fill: false\n' +
        '                },\n' +
        '                {\n' +
        '                    label: "Clothing",\n' +
        '                    data: [12000, 11000, 12500, 10500, 11500, 13000, 14000, 12500, 11000, 9500, 10000, 12000],\n' +
        '                    borderColor: "#1cc88a",\n' +
        '                    backgroundColor: "#1cc88a",\n' +
        '                    borderWidth: 2,\n' +
        '                    pointRadius: 5,\n' +
        '                    tension: 0,\n' +
        '                    fill: false\n' +
        '                },\n' +
        '                {\n' +
        '                    label: "Home Goods",\n' +
        '                    data: [8000, 8500, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 12500, 13000, 13500],\n' +
        '                    borderColor: "#36b9cc",\n' +
        '                    backgroundColor: "#36b9cc",\n' +
        '                    borderWidth: 2,\n' +
        '                    pointRadius: 5,\n' +
        '                    tension: 0,\n' +
        '                    fill: false\n' +
        '                }\n' +
        '            ]',
        f'datasets: {json.dumps(chart_data["datasets"], indent=16)}'
    ).replace(
        'Interactive Sales Trend Dashboard',
        title
    ).replace(
        'Monthly Sales Trend (2023)',
        title
    )

    # Save to plot directory as HTML
    charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    timestamp = str(int(time.time()))
    filename = f"chart_{timestamp}.html"
    filepath = os.path.join(charts_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(template)
    except Exception as e:
        return {
            "status": "ERROR",
            "error": "FILE_WRITE_ERROR",
            "message": str(e)
        }

    return {
        "status": "SUCCESS",
        "filepath": os.path.abspath(filepath)
    }


if __name__ == "__main__":
    mcp.run()
