# Testing Guide for Pandas MCP Server

This guide provides comprehensive information about the test suite for the pandas-mcp-server project.

## Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Writing Tests](#writing-tests)
- [Continuous Integration](#continuous-integration)

## Overview

The test suite includes:

- **Unit Tests**: Test individual functions and modules in isolation
- **Integration Tests**: Test interactions between multiple modules
- **End-to-End Tests**: Test complete workflows from start to finish

### Test Modules

| Test File | Description |
|-----------|-------------|
| `test_config.py` | Tests for configuration module and environment variable handling |
| `test_error_handling.py` | Tests for error handling utilities and response formatting |
| `test_execution.py` | Tests for pandas code execution and security validation |
| `test_visualization.py` | Tests for chart generation and visualization |
| `test_metadata.py` | Tests for file metadata extraction |
| `test_validation.py` | Tests for file validation functions |
| `test_integration.py` | Integration tests for complete workflows |

## Running Tests

### Prerequisites

Install test dependencies:

```bash
pip install -r requirements.txt
```

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_config.py
```

### Run Specific Test Class

```bash
pytest tests/test_execution.py::TestRunPandasCode
```

### Run Specific Test Method

```bash
pytest tests/test_execution.py::TestRunPandasCode::test_simple_pandas_code
```

### Run with Verbose Output

```bash
pytest -v
```

### Run with Coverage Report

```bash
pytest --cov=core --cov-report=html
```

This generates an HTML coverage report in `htmlcov/` directory.

### Run Only Unit Tests

```bash
pytest -m unit
```

### Run Only Integration Tests

```bash
pytest -m integration
```

### Exclude Slow Tests

```bash
pytest -m "not slow"
```

### Stop on First Failure

```bash
pytest -x
```

### Show Print Statements

```bash
pytest -s
```

## Test Coverage

### Current Coverage Areas

1. **Configuration Module**
   - Environment variable parsing (bool, int, list)
   - Default values and fallbacks
   - Configuration printing and debugging

2. **Error Handling Module**
   - Error type enumeration
   - Response formatting (success/error)
   - Exception handling and logging
   - Response validation

3. **Execution Module**
   - Security validation (blacklist checking)
   - Pandas code execution
   - Forbidden code detection
   - Error handling for invalid code

4. **Visualization Module**
   - Chart generation (bar, line, pie)
   - Data format validation
   - Custom options and styling
   - Error handling for invalid inputs

5. **Metadata Module**
   - File metadata extraction
   - Data type detection
   - Missing value detection
   - Support for CSV, Excel, JSON

6. **Validation Module**
   - File path validation
   - File size validation
   - File type validation
   - Edge case handling

7. **Integration Tests**
   - Complete data analysis workflows
   - Data cleaning workflows
   - Aggregation workflows
   - Time series analysis
   - Visualization integration

### Coverage Goals

- **Line Coverage**: Target > 80%
- **Branch Coverage**: Target > 70%
- **Function Coverage**: Target > 90%

## Writing Tests

### Test Structure

Follow this structure for new tests:

```python
"""Tests for [module_name]."""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.module_name import function_to_test


class TestClassName:
    """Test class description."""
    
    def test_method_name(self):
        """Test method description."""
        # Arrange
        input_data = ...
        
        # Act
        result = function_to_test(input_data)
        
        # Assert
        assert result == expected_value
    
    def test_edge_case(self):
        """Test edge case description."""
        # Test implementation
        pass
```

### Best Practices

1. **Use Descriptive Names**: Test names should clearly describe what is being tested
2. **Follow AAA Pattern**: Arrange, Act, Assert
3. **Test Edge Cases**: Include tests for boundary conditions and edge cases
4. **Use Fixtures**: Leverage pytest fixtures for common setup
5. **Keep Tests Independent**: Each test should be able to run independently
6. **Mock External Dependencies**: Use mocks for external services or I/O

### Using Fixtures

```python
import pytest
import pandas as pd
from pathlib import Path


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing."""
    return pd.DataFrame({
        'a': [1, 2, 3],
        'b': [4, 5, 6]
    })


@pytest.fixture
def temp_csv_file(tmp_path):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test.csv"
    df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
    df.to_csv(csv_file, index=False)
    return str(csv_file)


def test_with_fixture(sample_dataframe, temp_csv_file):
    """Test using fixtures."""
    # Test implementation
    pass
```

### Testing Error Cases

```python
def test_error_handling():
    """Test that errors are handled correctly."""
    with pytest.raises(ValueError):
        function_that_raises_value_error()
    
    # Or test error response
    response = function_that_returns_error()
    assert response['success'] is False
    assert 'error' in response
```

### Testing with Temporary Files

```python
def test_with_temp_file(tmp_path):
    """Test using temporary directory."""
    # tmp_path is a pytest fixture
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    # Use the file
    result = process_file(str(test_file))
    assert result is not None
```

## Test Markers

Use pytest markers to categorize tests:

```python
import pytest


@pytest.mark.unit
def test_unit_function():
    """Unit test marker."""
    pass


@pytest.mark.integration
def test_integration_workflow():
    """Integration test marker."""
    pass


@pytest.mark.slow
def test_slow_operation():
    """Slow test marker."""
    pass
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=core --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running tests from the project root directory
2. **Path Issues**: Tests add parent directory to sys.path automatically
3. **Missing Dependencies**: Install all requirements with `pip install -r requirements.txt`
4. **Temporary Files**: Use pytest's `tmp_path` fixture for temporary files

### Debugging Failed Tests

Run with verbose output and stop on first failure:

```bash
pytest -v -x --tb=long
```

Use Python debugger:

```python
def test_debugging():
    import pdb; pdb.set_trace()
    # Test code
```

### Running Tests in Parallel

Install pytest-xdist:

```bash
pip install pytest-xdist
```

Run tests in parallel:

```bash
pytest -n auto
```

## Contributing

When adding new features:

1. Write tests before implementing the feature (TDD approach)
2. Ensure all tests pass before submitting a PR
3. Maintain or improve test coverage
4. Add integration tests for new workflows
5. Update this documentation if needed

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
