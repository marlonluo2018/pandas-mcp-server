"""Unit tests for error handling module."""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.error_handling import (
    ErrorType,
    create_error_response,
    create_success_response,
    handle_exception,
    log_and_return_error,
    validate_response_format
)


class TestErrorType:
    """Test ErrorType enum."""
    
    def test_error_type_values(self):
        """Test that all ErrorType enum values are defined."""
        assert ErrorType.FILE_NOT_FOUND.value == "FILE_NOT_FOUND"
        assert ErrorType.INVALID_INPUT.value == "INVALID_INPUT"
        assert ErrorType.SECURITY_VIOLATION.value == "SECURITY_VIOLATION"
        assert ErrorType.TOOL_EXECUTION_ERROR.value == "TOOL_EXECUTION_ERROR"
        assert ErrorType.FEATURE_DISABLED.value == "FEATURE_DISABLED"
        assert ErrorType.UNKNOWN_ERROR.value == "UNKNOWN_ERROR"
    
    def test_error_type_count(self):
        """Test that we have the expected number of error types."""
        # Count the error types
        error_types = [
            'FILE_NOT_FOUND', 'INVALID_FILE_PATH', 'FILE_TOO_LARGE', 'UNSUPPORTED_FILE_TYPE',
            'INVALID_COLUMN_NAMES', 'INVALID_SHEET_NAME', 'INVALID_CODE', 'INVALID_INPUT',
            'SECURITY_VIOLATION', 'CODE_EXECUTION_ERROR', 'CODE_COMPILATION_ERROR',
            'DATA_ERROR', 'TOOL_EXECUTION_ERROR', 'FEATURE_DISABLED',
            'UNKNOWN_ERROR', 'INTERNAL_ERROR'
        ]
        assert len(ErrorType) == len(error_types)


class TestCreateErrorResponse:
    """Test create_error_response function."""
    
    def test_basic_error_response(self):
        """Test creating a basic error response."""
        response = create_error_response(
            ErrorType.INVALID_INPUT,
            "Test error message"
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "INVALID_INPUT"
        assert response["message"] == "Test error message"
        assert "details" not in response
        assert "traceback" not in response
    
    def test_error_response_with_details(self):
        """Test creating error response with details."""
        details = {"field": "value", "count": 5}
        response = create_error_response(
            ErrorType.FILE_NOT_FOUND,
            "File not found",
            details=details
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "FILE_NOT_FOUND"
        assert response["message"] == "File not found"
        assert response["details"] == details
    
    def test_error_response_with_traceback(self):
        """Test creating error response with traceback."""
        traceback_str = "Traceback (most recent call last):\n  ..."
        response = create_error_response(
            ErrorType.UNKNOWN_ERROR,
            "Unknown error",
            traceback=traceback_str
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "UNKNOWN_ERROR"
        assert response["message"] == "Unknown error"
        assert response["traceback"] == traceback_str
    
    def test_error_response_with_all_fields(self):
        """Test creating error response with all fields."""
        details = {"field": "value"}
        traceback_str = "Traceback (most recent call last):\n  ..."
        response = create_error_response(
            ErrorType.TOOL_EXECUTION_ERROR,
            "Tool failed",
            details=details,
            traceback=traceback_str
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "TOOL_EXECUTION_ERROR"
        assert response["message"] == "Tool failed"
        assert response["details"] == details
        assert response["traceback"] == traceback_str


class TestCreateSuccessResponse:
    """Test create_success_response function."""
    
    def test_basic_success_response(self):
        """Test creating a basic success response."""
        data = {"key": "value"}
        response = create_success_response(data)
        
        assert response["status"] == "SUCCESS"
        assert response["data"] == data
        assert "metadata" not in response
    
    def test_success_response_with_metadata(self):
        """Test creating success response with metadata."""
        data = {"result": 42}
        metadata = {"count": 10, "time": 1.5}
        response = create_success_response(data, metadata=metadata)
        
        assert response["status"] == "SUCCESS"
        assert response["data"] == data
        assert response["metadata"] == metadata
    
    def test_success_response_with_none_data(self):
        """Test creating success response with None data."""
        response = create_success_response(None)
        
        assert response["status"] == "SUCCESS"
        assert response["data"] is None


class TestHandleException:
    """Test handle_exception function."""
    
    def test_handle_basic_exception(self):
        """Test handling a basic exception."""
        error = ValueError("Invalid value")
        response = handle_exception(
            error,
            ErrorType.INVALID_INPUT,
            "Validation failed"
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "INVALID_INPUT"
        assert "Validation failed" in response["message"]
        assert "Invalid value" in response["message"]
        assert "traceback" in response
    
    def test_handle_exception_without_context(self):
        """Test handling exception without context."""
        error = RuntimeError("Runtime error")
        response = handle_exception(error)
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "UNKNOWN_ERROR"
        assert "Runtime error" in response["message"]
    
    def test_handle_exception_no_traceback(self):
        """Test handling exception without traceback."""
        error = KeyError("Missing key")
        response = handle_exception(
            error,
            ErrorType.DATA_ERROR,
            "Data error",
            include_traceback=False
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "DATA_ERROR"
        assert "traceback" not in response
    
    def test_handle_exception_custom_error_type(self):
        """Test handling exception with custom error type."""
        error = FileNotFoundError("File not found")
        response = handle_exception(
            error,
            ErrorType.FILE_NOT_FOUND,
            "File access failed"
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "FILE_NOT_FOUND"


class TestLogAndReturnError:
    """Test log_and_return_error function."""
    
    def test_log_and_return_basic_error(self):
        """Test logging and returning a basic error."""
        response = log_and_return_error(
            ErrorType.SECURITY_VIOLATION,
            "Security check failed"
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "SECURITY_VIOLATION"
        assert response["message"] == "Security check failed"
        assert "details" not in response
    
    def test_log_and_return_error_with_details(self):
        """Test logging and returning error with details."""
        details = {"attempted_operation": "eval"}
        response = log_and_return_error(
            ErrorType.SECURITY_VIOLATION,
            "Forbidden operation",
            details=details
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "SECURITY_VIOLATION"
        assert response["details"] == details
    
    def test_log_and_return_feature_disabled_error(self):
        """Test logging and returning feature disabled error."""
        response = log_and_return_error(
            ErrorType.FEATURE_DISABLED,
            "Chart generation is disabled"
        )
        
        assert response["status"] == "ERROR"
        assert response["error_type"] == "FEATURE_DISABLED"
        assert response["message"] == "Chart generation is disabled"


class TestValidateResponseFormat:
    """Test validate_response_format function."""
    
    def test_valid_error_response(self):
        """Test validating a valid error response."""
        response = create_error_response(
            ErrorType.INVALID_INPUT,
            "Invalid input"
        )
        assert validate_response_format(response) is True
    
    def test_valid_success_response(self):
        """Test validating a valid success response."""
        response = create_success_response({"data": "value"})
        assert validate_response_format(response) is True
    
    def test_invalid_response_not_dict(self):
        """Test validating non-dict response."""
        assert validate_response_format("not a dict") is False
        assert validate_response_format(123) is False
        assert validate_response_format(None) is False
    
    def test_invalid_response_missing_status(self):
        """Test validating response without status."""
        response = {"error_type": "INVALID_INPUT", "message": "Error"}
        assert validate_response_format(response) is False
    
    def test_invalid_response_invalid_status(self):
        """Test validating response with invalid status."""
        response = {"status": "PENDING", "data": {}}
        assert validate_response_format(response) is False
    
    def test_invalid_error_response_missing_fields(self):
        """Test validating error response without required fields."""
        response = {"status": "ERROR", "message": "Error"}
        assert validate_response_format(response) is False
    
    def test_invalid_success_response_missing_data(self):
        """Test validating success response without data."""
        response = {"status": "SUCCESS"}
        assert validate_response_format(response) is False
    
    def test_valid_response_with_metadata(self):
        """Test validating response with optional metadata."""
        response = create_success_response({"data": "value"}, {"count": 5})
        assert validate_response_format(response) is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
