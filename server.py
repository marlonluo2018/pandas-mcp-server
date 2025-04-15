from mcp.server.fastmcp import FastMCP

import traceback  

mcp = FastMCP("PandasAgent")


@mcp.tool()
def load_csv_tool(file_path: str) -> dict:
    """
    MCP专用CSV加载工具（解决框架集成问题）
    
    特殊处理：
    1. 强制UTF-8编码读取
    2. 限制最大文件大小（10MB）
    3. 返回MCP兼容的简化格式
    """
    import pandas as pd
    import os
    from chardet import detect
    import traceback

    # MCP环境专用配置
    MCP_MAX_SIZE = 10 * 1024 * 1024  # 10MB
    
    try:
        # 验证文件基础信息（MCP环境可能权限不同）
        if not os.path.exists(file_path):
            return {"error": "FILE_NOT_FOUND", "path": file_path}
            
        if os.path.getsize(file_path) > MCP_MAX_SIZE:
            return {"error": "FILE_TOO_LARGE", "max_size": f"{MCP_MAX_SIZE/1024/1024}MB"}

        # MCP环境下更可靠的编码检测
        with open(file_path, 'rb') as f:
            rawdata = f.read(50000)  # 50KB足够检测编码
            enc = detect(rawdata)['encoding'] or 'utf-8'
        
        # 使用更安全的读取方式
        df = pd.read_csv(
            file_path,
            encoding=enc,
            nrows=100,  # 仅读取前100行分析
            on_bad_lines='skip'  # 自动跳过问题行
        )
        
        # 返回MCP专用简化格式
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
                "size": f"{os.path.getsize(file_path)/1024:.1f}KB",
                "encoding": enc
            }
        }

    except Exception as e:
        # MCP需要的错误格式
        return {
            "status": "ERROR",
            "error_type": type(e).__name__,
            "message": str(e),
            "solution": [
                "检查文件是否被其他程序占用",
                "尝试重新保存为UTF-8编码的CSV",
                "联系管理员查看MCP文件访问权限"
            ]
        }


@mcp.tool()
def run_pandas_code(code: str) -> dict:
    """
    Execute pandas code with smart suggestions
    
    Requirements:
    - Must contain full import and file loading logic
    - Must assign final result to 'result' variable
    
    Smart Suggestions:
    1. For string columns: 
       df['col'] = df['col'].astype(str).str.strip()
    2. For numeric comparisons:
       df['col'] = pd.to_numeric(df['col'], errors='coerce')
    3. For path handling:
       Use raw strings: r"path\\to\\file.csv"
    4. For null handling:
       .fillna() before operations
    
    Example Correct Code:
    import pandas as pd
    df = pd.read_csv(r"path\\to\\file.csv")
    df['Category'] = df['Category'].astype(str).str.strip()
    result = df[df['Category'] == 'D'].shape[0]
    """
    import pandas as pd
    import traceback
    from io import StringIO
    import sys
    import re

    # Prepare execution
    local_vars = {'pd': pd}
    stdout_capture = StringIO()
    suggestions = []

    # Analyze code for common issues
    if not re.search(r'\.astype$str$', code):
        suggestions.append("Consider adding .astype(str) for string columns")
    if not re.search(r'\.str\.strip$$', code):
        suggestions.append("Consider adding .str.strip() to clean strings")
    if '\\' in code and not 'r"' in code:
        suggestions.append("Use raw strings (r\"path\") for Windows paths")

    # Execute
    old_stdout = sys.stdout
    sys.stdout = stdout_capture
    
    try:
        exec(code, {}, local_vars)
        result = local_vars.get('result', None)
        
        if result is not None:
            response = {"result": str(result)}
            if suggestions:
                response["suggestions"] = suggestions
            return response
            
        return {
            "error": "No result variable set",
            "output": stdout_capture.getvalue(),
            "solution": "Add 'result = ' before your final calculation",
            "suggestions": suggestions
        }
        
    except Exception as e:
        # Generate specific suggestions based on error
        error_suggestions = suggestions.copy()
        if "Cannot compare" in str(e):
            error_suggestions.append("Convert column types before comparison")
        if "NoneType" in str(e):
            error_suggestions.append("Handle null values using .fillna()")
        
        return {
            "error": {
                "type": type(e).__name__,
                "message": str(e),
                "traceback": traceback.format_exc(),
                "suggestions": error_suggestions,
                "output": stdout_capture.getvalue()
            }
        }
    finally:
        sys.stdout = old_stdout


if __name__ == "__main__":
    mcp.run()