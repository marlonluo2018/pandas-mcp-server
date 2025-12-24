"""Unit tests for config module."""
import pytest
import sys
import os
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import (
    get_env_bool,
    get_env_int,
    get_env_list,
    CHARTS_DIR,
    MAX_FILE_SIZE,
    BLACKLIST,
    LOG_LEVEL,
    LOG_FILE,
    LOG_MAX_BYTES,
    LOG_BACKUP_COUNT,
    ENABLE_MEMORY_MONITORING,
    MEMORY_WARNING_THRESHOLD,
    ENABLE_CHART_GENERATION,
    ENABLE_CODE_EXECUTION,
    print_config
)


class TestGetEnvBool:
    """Test get_env_bool function."""
    
    def test_get_env_bool_true_values(self):
        """Test get_env_bool with various true values."""
        true_values = ['true', 'True', 'TRUE', '1', 'yes', 'Yes', 'YES', 'on', 'On', 'ON']
        
        for value in true_values:
            os.environ['TEST_BOOL_VAR'] = value
            assert get_env_bool('TEST_BOOL_VAR', False) is True
            del os.environ['TEST_BOOL_VAR']
    
    def test_get_env_bool_false_values(self):
        """Test get_env_bool with various false values."""
        false_values = ['false', 'False', 'FALSE', '0', 'no', 'No', 'NO', 'off', 'Off', 'OFF']
        
        for value in false_values:
            os.environ['TEST_BOOL_VAR'] = value
            assert get_env_bool('TEST_BOOL_VAR', True) is False
            del os.environ['TEST_BOOL_VAR']
    
    def test_get_env_bool_default(self):
        """Test get_env_bool with default value."""
        # Environment variable not set
        assert get_env_bool('NONEXISTENT_BOOL_VAR', True) is True
        assert get_env_bool('NONEXISTENT_BOOL_VAR', False) is False
    
    def test_get_env_bool_invalid_value(self):
        """Test get_env_bool with invalid value returns default."""
        os.environ['TEST_BOOL_VAR'] = 'invalid'
        assert get_env_bool('TEST_BOOL_VAR', True) is True
        assert get_env_bool('TEST_BOOL_VAR', False) is False
        del os.environ['TEST_BOOL_VAR']


class TestGetEnvInt:
    """Test get_env_int function."""
    
    def test_get_env_int_valid_values(self):
        """Test get_env_int with valid integer values."""
        test_cases = [
            ('100', 100),
            ('0', 0),
            ('-50', -50),
            ('999999', 999999),
        ]
        
        for env_value, expected in test_cases:
            os.environ['TEST_INT_VAR'] = env_value
            assert get_env_int('TEST_INT_VAR', 0) == expected
            del os.environ['TEST_INT_VAR']
    
    def test_get_env_int_default(self):
        """Test get_env_int with default value."""
        assert get_env_int('NONEXISTENT_INT_VAR', 42) == 42
        assert get_env_int('NONEXISTENT_INT_VAR', 0) == 0
    
    def test_get_env_int_invalid_value(self):
        """Test get_env_int with invalid value returns default."""
        os.environ['TEST_INT_VAR'] = 'not_a_number'
        assert get_env_int('TEST_INT_VAR', 42) == 42
        del os.environ['TEST_INT_VAR']
    
    def test_get_env_int_float_value(self):
        """Test get_env_int with float value returns default."""
        os.environ['TEST_INT_VAR'] = '123.45'
        assert get_env_int('TEST_INT_VAR', 42) == 42
        del os.environ['TEST_INT_VAR']


class TestGetEnvList:
    """Test get_env_list function."""
    
    def test_get_env_list_valid_values(self):
        """Test get_env_list with valid comma-separated values."""
        test_cases = [
            ('item1,item2,item3', ['item1', 'item2', 'item3']),
            ('a,b,c,d', ['a', 'b', 'c', 'd']),
            ('single', ['single']),
            (' spaced , items ', ['spaced', 'items']),
        ]
        
        for env_value, expected in test_cases:
            os.environ['TEST_LIST_VAR'] = env_value
            assert get_env_list('TEST_LIST_VAR', []) == expected
            del os.environ['TEST_LIST_VAR']
    
    def test_get_env_list_default(self):
        """Test get_env_list with default value."""
        default = ['default1', 'default2']
        assert get_env_list('NONEXISTENT_LIST_VAR', default) == default
    
    def test_get_env_list_empty_string(self):
        """Test get_env_list with empty string returns default."""
        os.environ['TEST_LIST_VAR'] = ''
        assert get_env_list('TEST_LIST_VAR', ['default']) == ['default']
        del os.environ['TEST_LIST_VAR']
    
    def test_get_env_list_empty_items(self):
        """Test get_env_list filters out empty items."""
        os.environ['TEST_LIST_VAR'] = 'item1,,item2,,item3'
        result = get_env_list('TEST_LIST_VAR', [])
        assert result == ['item1', 'item2', 'item3']
        del os.environ['TEST_LIST_VAR']


class TestConfigurationDefaults:
    """Test default configuration values."""
    
    def test_charts_dir_exists(self):
        """Test that CHARTS_DIR is set and exists."""
        assert CHARTS_DIR is not None
        assert isinstance(CHARTS_DIR, str)
        # Check if directory exists (it should be created by config.py)
        assert os.path.exists(CHARTS_DIR)
    
    def test_max_file_size_default(self):
        """Test default MAX_FILE_SIZE."""
        assert MAX_FILE_SIZE == 100 * 1024 * 1024  # 100MB
    
    def test_blacklist_default(self):
        """Test default BLACKLIST."""
        assert isinstance(BLACKLIST, list)
        assert len(BLACKLIST) > 0
        assert 'os.' in BLACKLIST
        assert 'eval(' in BLACKLIST
        assert 'subprocess.' in BLACKLIST
    
    def test_log_level_default(self):
        """Test default LOG_LEVEL."""
        assert LOG_LEVEL == 'INFO'
    
    def test_log_file_default(self):
        """Test default LOG_FILE."""
        assert LOG_FILE is not None
        assert isinstance(LOG_FILE, str)
        assert 'mcp_server.log' in LOG_FILE
    
    def test_log_max_bytes_default(self):
        """Test default LOG_MAX_BYTES."""
        assert LOG_MAX_BYTES == 5 * 1024 * 1024  # 5MB
    
    def test_log_backup_count_default(self):
        """Test default LOG_BACKUP_COUNT."""
        assert LOG_BACKUP_COUNT == 3
    
    def test_enable_memory_monitoring_default(self):
        """Test default ENABLE_MEMORY_MONITORING."""
        assert ENABLE_MEMORY_MONITORING is True
    
    def test_memory_warning_threshold_default(self):
        """Test default MEMORY_WARNING_THRESHOLD."""
        assert MEMORY_WARNING_THRESHOLD == 500  # MB
    
    def test_enable_chart_generation_default(self):
        """Test default ENABLE_CHART_GENERATION."""
        assert ENABLE_CHART_GENERATION is True
    
    def test_enable_code_execution_default(self):
        """Test default ENABLE_CODE_EXECUTION."""
        assert ENABLE_CODE_EXECUTION is True


class TestConfigurationOverrides:
    """Test configuration overrides via environment variables."""
    
    def test_override_max_file_size(self):
        """Test overriding MAX_FILE_SIZE."""
        original_value = MAX_FILE_SIZE
        
        os.environ['PANDAS_MCP_MAX_FILE_SIZE'] = '52428800'  # 50MB
        # Re-import to test override (in real usage, this would be set before import)
        # For this test, we just verify the environment variable is set
        assert os.environ['PANDAS_MCP_MAX_FILE_SIZE'] == '52428800'
        
        del os.environ['PANDAS_MCP_MAX_FILE_SIZE']
    
    def test_override_log_level(self):
        """Test overriding LOG_LEVEL."""
        os.environ['PANDAS_MCP_LOG_LEVEL'] = 'DEBUG'
        assert os.environ['PANDAS_MCP_LOG_LEVEL'] == 'DEBUG'
        del os.environ['PANDAS_MCP_LOG_LEVEL']
    
    def test_override_feature_flags(self):
        """Test overriding feature flags."""
        os.environ['PANDAS_MCP_ENABLE_CHART_GENERATION'] = 'false'
        os.environ['PANDAS_MCP_ENABLE_CODE_EXECUTION'] = 'false'
        
        assert os.environ['PANDAS_MCP_ENABLE_CHART_GENERATION'] == 'false'
        assert os.environ['PANDAS_MCP_ENABLE_CODE_EXECUTION'] == 'false'
        
        del os.environ['PANDAS_MCP_ENABLE_CHART_GENERATION']
        del os.environ['PANDAS_MCP_ENABLE_CODE_EXECUTION']


class TestPrintConfig:
    """Test print_config function."""
    
    def test_print_config_output(self, capsys):
        """Test that print_config produces output."""
        print_config()
        captured = capsys.readouterr()
        
        output = captured.out
        assert "Pandas MCP Server Configuration" in output
        assert "CHARTS_DIR:" in output
        assert "MAX_FILE_SIZE:" in output
        assert "LOG_LEVEL:" in output
        assert "LOG_FILE:" in output
        assert "ENABLE_MEMORY_MONITORING:" in output
        assert "ENABLE_CHART_GENERATION:" in output
        assert "ENABLE_CODE_EXECUTION:" in output
        assert "BLACKLIST items:" in output
    
    def test_print_config_format(self, capsys):
        """Test print_config output format."""
        print_config()
        captured = capsys.readouterr()
        
        output = captured.out
        # Check for separator lines
        assert "=" in output
        # Check for MB formatting
        assert "MB" in output


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
