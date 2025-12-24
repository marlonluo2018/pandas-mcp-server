"""Input validation utilities for pandas-mcp-server."""
import os
import re
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.csv', '.xlsx', '.xls'}

# Maximum file path length
MAX_PATH_LENGTH = 260  # Windows MAX_PATH

# Pattern for valid column names (alphanumeric, underscores, spaces, hyphens)
VALID_COLUMN_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\s\-]+$')


def validate_file_path(file_path: str) -> dict:
    """
    Validate file path for security and correctness.
    
    Args:
        file_path: Path to validate
        
    Returns:
        dict: Validation result with 'valid' boolean and 'error' message if invalid
    """
    if not file_path:
        return {
            'valid': False,
            'error': 'File path cannot be empty'
        }
    
    if not isinstance(file_path, str):
        return {
            'valid': False,
            'error': f'File path must be a string, got {type(file_path).__name__}'
        }
    
    # Check path length
    if len(file_path) > MAX_PATH_LENGTH:
        return {
            'valid': False,
            'error': f'File path exceeds maximum length of {MAX_PATH_LENGTH} characters'
        }
    
    # Normalize path
    try:
        normalized_path = os.path.normpath(file_path)
    except Exception as e:
        return {
            'valid': False,
            'error': f'Invalid path format: {str(e)}'
        }
    
    # Check for path traversal attempts
    if '..' in normalized_path.split(os.sep):
        logger.warning(f"Potential path traversal attempt detected: {file_path}")
        return {
            'valid': False,
            'error': 'Path traversal is not allowed'
        }
    
    # Check file extension
    _, ext = os.path.splitext(normalized_path)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return {
            'valid': False,
            'error': f'Unsupported file type: {ext}. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }
    
    # Check if file exists (optional - may be disabled for pre-validation)
    if not os.path.exists(normalized_path):
        return {
            'valid': False,
            'error': f'File not found: {normalized_path}'
        }
    
    # Check if it's a file (not a directory)
    if not os.path.isfile(normalized_path):
        return {
            'valid': False,
            'error': f'Path is not a file: {normalized_path}'
        }
    
    return {'valid': True}


def validate_column_names(column_names: List[str]) -> dict:
    """
    Validate column names for security and correctness.
    
    Args:
        column_names: List of column names to validate
        
    Returns:
        dict: Validation result with 'valid' boolean and 'error' message if invalid
    """
    if not column_names:
        return {
            'valid': False,
            'error': 'Column names list cannot be empty'
        }
    
    if not isinstance(column_names, list):
        return {
            'valid': False,
            'error': f'Column names must be a list, got {type(column_names).__name__}'
        }
    
    if len(column_names) > 100:
        return {
            'valid': False,
            'error': 'Cannot process more than 100 columns at once'
        }
    
    for i, col_name in enumerate(column_names):
        if not isinstance(col_name, str):
            return {
                'valid': False,
                'error': f'Column name at index {i} must be a string, got {type(col_name).__name__}'
            }
        
        if not col_name.strip():
            return {
                'valid': False,
                'error': f'Column name at index {i} cannot be empty or whitespace only'
            }
        
        if len(col_name) > 255:
            return {
                'valid': False,
                'error': f'Column name at index {i} exceeds maximum length of 255 characters'
            }
        
        # Check for SQL injection patterns
        sql_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'INSERT', 'UPDATE', 'EXEC', 'SELECT']
        upper_name = col_name.upper()
        for keyword in sql_keywords:
            if keyword in upper_name:
                logger.warning(f"Potential SQL injection pattern detected in column name: {col_name}")
                return {
                    'valid': False,
                    'error': f'Column name contains potentially dangerous pattern: {keyword}'
                }
        
        # Check for shell metacharacters
        shell_chars = ['|', '&', ';', '$', '`', '(', ')', '<', '>', '!']
        if any(char in col_name for char in shell_chars):
            logger.warning(f"Shell metacharacter detected in column name: {col_name}")
            return {
                'valid': False,
                'error': 'Column name contains invalid characters'
            }
    
    return {'valid': True}


def validate_sheet_name(sheet_name: Optional[str] = None) -> dict:
    """
    Validate Excel sheet name.
    
    Args:
        sheet_name: Sheet name or index to validate
        
    Returns:
        dict: Validation result with 'valid' boolean and 'error' message if invalid
    """
    if sheet_name is None:
        return {'valid': True}
    
    if isinstance(sheet_name, int):
        if sheet_name < 0:
            return {
                'valid': False,
                'error': 'Sheet index cannot be negative'
            }
        if sheet_name > 1000:
            return {
                'valid': False,
                'error': 'Sheet index exceeds reasonable limit'
            }
        return {'valid': True}
    
    if isinstance(sheet_name, str):
        if not sheet_name.strip():
            return {
                'valid': False,
                'error': 'Sheet name cannot be empty'
            }
        
        if len(sheet_name) > 31:
            return {
                'valid': False,
                'error': 'Excel sheet name cannot exceed 31 characters'
            }
        
        # Excel sheet name restrictions
        invalid_chars = ['\\', '/', '*', '?', ':', '[', ']']
        if any(char in sheet_name for char in invalid_chars):
            return {
                'valid': False,
                'error': f'Sheet name contains invalid Excel characters: {", ".join(invalid_chars)}'
            }
        
        return {'valid': True}
    
    return {
        'valid': False,
        'error': f'Sheet name must be a string or integer, got {type(sheet_name).__name__}'
    }


def validate_pandas_code(code: str) -> dict:
    """
    Validate pandas code for basic security and syntax.
    
    Args:
        code: Python code string to validate
        
    Returns:
        dict: Validation result with 'valid' boolean and 'error' message if invalid
    """
    if not code:
        return {
            'valid': False,
            'error': 'Code cannot be empty'
        }
    
    if not isinstance(code, str):
        return {
            'valid': False,
            'error': f'Code must be a string, got {type(code).__name__}'
        }
    
    # Check code length
    if len(code) > 100000:  # 100KB limit
        return {
            'valid': False,
            'error': 'Code exceeds maximum length of 100KB'
        }
    
    # Check for basic syntax errors
    try:
        compile(code, '<string>', 'exec')
    except SyntaxError as e:
        return {
            'valid': False,
            'error': f'Syntax error in code: {str(e)}'
        }
    
    return {'valid': True}