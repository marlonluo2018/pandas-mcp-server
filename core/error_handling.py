"""Standardized error handling utilities for pandas-mcp-server."""
import logging
from typing import Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ErrorType(Enum):
    """Enumeration of standard error types."""
    # File-related errors
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    INVALID_FILE_PATH = "INVALID_FILE_PATH"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UNSUPPORTED_FILE_TYPE = "UNSUPPORTED_FILE_TYPE"
    
    # Input validation errors
    INVALID_COLUMN_NAMES = "INVALID_COLUMN_NAMES"
    INVALID_SHEET_NAME = "INVALID_SHEET_NAME"
    INVALID_CODE = "INVALID_CODE"
    INVALID_INPUT = "INVALID_INPUT"
    
    # Security errors
    SECURITY_VIOLATION = "SECURITY_VIOLATION"
    
    # Execution errors
    CODE_EXECUTION_ERROR = "CODE_EXECUTION_ERROR"
    CODE_COMPILATION_ERROR = "CODE_COMPILATION_ERROR"
    
    # Data errors
    DATA_ERROR = "DATA_ERROR"
    
    # Tool errors
    TOOL_EXECUTION_ERROR = "TOOL_EXECUTION_ERROR"
    
    # Feature errors
    FEATURE_DISABLED = "FEATURE_DISABLED"
    
    # Generic errors
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


def create_error_response(
    error_type: ErrorType,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    traceback: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        error_type: Type of error from ErrorType enum
        message: Human-readable error message
        details: Additional error details (optional)
        traceback: Exception traceback (optional)
        
    Returns:
        dict: Standardized error response
    """
    error_response = {
        "status": "ERROR",
        "error_type": error_type.value,
        "message": message
    }
    
    if details:
        error_response["details"] = details
    
    if traceback:
        error_response["traceback"] = traceback
    
    return error_response


def create_success_response(data: Any, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        metadata: Optional metadata about the response
        
    Returns:
        dict: Standardized success response
    """
    response = {
        "status": "SUCCESS",
        "data": data
    }
    
    if metadata:
        response["metadata"] = metadata
    
    return response


def handle_exception(
    error: Exception,
    error_type: ErrorType = ErrorType.UNKNOWN_ERROR,
    context: Optional[str] = None,
    include_traceback: bool = True
) -> Dict[str, Any]:
    """
    Handle an exception and return a standardized error response.
    
    Args:
        error: The exception to handle
        error_type: Type of error (defaults to UNKNOWN_ERROR)
        context: Additional context about where the error occurred
        include_traceback: Whether to include the traceback
        
    Returns:
        dict: Standardized error response
    """
    error_message = str(error)
    
    if context:
        error_message = f"{context}: {error_message}"
        logger.error(f"{context}: {type(error).__name__}: {error_message}")
    else:
        logger.error(f"{type(error).__name__}: {error_message}")
    
    response = create_error_response(
        error_type=error_type,
        message=error_message
    )
    
    if include_traceback:
        import traceback as tb
        response["traceback"] = tb.format_exc()
        logger.debug(f"Traceback:\n{response['traceback']}")
    
    return response


def log_and_return_error(
    error_type: ErrorType,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    level: str = "error"
) -> Dict[str, Any]:
    """
    Log an error and return a standardized error response.
    
    Args:
        error_type: Type of error
        message: Error message
        details: Additional error details
        level: Log level (error, warning, info, debug)
        
    Returns:
        dict: Standardized error response
    """
    log_func = getattr(logger, level, logger.error)
    log_func(f"{error_type.value}: {message}")
    
    return create_error_response(
        error_type=error_type,
        message=message,
        details=details
    )


def validate_response_format(response: Dict[str, Any]) -> bool:
    """
    Validate that a response follows the standardized format.
    
    Args:
        response: Response to validate
        
    Returns:
        bool: True if response is valid, False otherwise
    """
    if not isinstance(response, dict):
        return False
    
    if "status" not in response:
        return False
    
    if response["status"] not in ["SUCCESS", "ERROR"]:
        return False
    
    if response["status"] == "ERROR":
        if "error_type" not in response or "message" not in response:
            return False
    else:
        if "data" not in response:
            return False
    
    return True
