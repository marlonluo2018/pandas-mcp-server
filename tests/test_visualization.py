"""Unit tests for visualization module."""
import pytest
import sys
import os
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.visualization import generate_chartjs
from core.error_handling import ErrorType


class TestGenerateChartJS:
    """Test generate_chartjs function."""
    
    def test_bar_chart_basic(self):
        """Test basic bar chart generation."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C', 'D']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30, 40]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Bar Chart'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_line_chart_basic(self):
        """Test basic line chart generation."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['Jan', 'Feb', 'Mar', 'Apr']
                },
                {
                    'name': 'Sales',
                    'type': 'number',
                    'examples': [100, 150, 200, 175]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['line'],
            title='Line Chart'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_pie_chart_basic(self):
        """Test basic pie chart generation."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['Red', 'Blue', 'Yellow']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [300, 50, 100]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['pie'],
            title='Pie Chart'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_chart_with_title(self):
        """Test chart generation with custom title."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='My Custom Chart'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_chart_with_custom_colors(self):
        """Test chart generation with custom colors."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Chart with Colors'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_multiple_datasets(self):
        """Test chart with multiple datasets."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C', 'D']
                },
                {
                    'name': 'Dataset1',
                    'type': 'number',
                    'examples': [10, 20, 30, 40]
                },
                {
                    'name': 'Dataset2',
                    'type': 'number',
                    'examples': [40, 30, 20, 10]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Multiple Datasets'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_chart_with_axes_options(self):
        """Test chart with custom axes options."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Chart with Axes',
            request_params={'yaxis_min': ['0']}
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_line_chart_with_fill(self):
        """Test line chart with fill option."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['Jan', 'Feb', 'Mar']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 15]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['line'],
            title='Line Chart with Fill'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_missing_chart_type(self):
        """Test error handling when chart type is missing."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=None,
            title='Test'
        )
        
        assert response['status'] == 'ERROR'
        assert 'error_type' in response
        assert 'message' in response
    
    def test_invalid_data_format(self):
        """Test error handling for invalid data format."""
        data = {
            'labels': ['A', 'B', 'C']
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Test'
        )
        
        assert response['status'] == 'ERROR'
        assert 'error_type' in response
        assert 'message' in response
    
    def test_empty_labels(self):
        """Test chart with empty labels."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': []
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': []
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Empty Chart'
        )
        
        assert 'status' in response
    
    def test_empty_datasets(self):
        """Test chart with empty datasets."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Empty Datasets'
        )
        
        assert 'status' in response
    
    def test_chart_html_structure(self):
        """Test that chart HTML has proper structure."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Structure Test'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_chart_config_structure(self):
        """Test that chart config has proper structure."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Config Test'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_pie_chart_colors(self):
        """Test pie chart with different colors."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['Red', 'Blue', 'Yellow']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [300, 50, 100]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['pie'],
            title='Pie Colors'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_responsive_option(self):
        """Test chart with responsive option."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Responsive Chart'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_legend_options(self):
        """Test chart with legend options."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Legend Test'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_tooltip_options(self):
        """Test chart with tooltip options."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Tooltip Test'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response


class TestVisualizationDataFormats:
    """Test different data format handling."""
    
    def test_dataframe_to_chart_format(self):
        """Test converting DataFrame to chart format."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='DataFrame Format'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_numeric_labels(self):
        """Test chart with numeric labels."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': [1, 2, 3, 4]
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30, 40]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Numeric Labels'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_float_values(self):
        """Test chart with float values."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10.5, 20.3, 30.7]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Float Values'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_negative_values(self):
        """Test chart with negative values."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [-10, 20, -30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Negative Values'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_zero_values(self):
        """Test chart with zero values."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [0, 20, 0]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Zero Values'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response


class TestChartErrorHandling:
    """Test error handling in chart generation."""
    
    def test_invalid_chart_type(self):
        """Test error handling for invalid chart type."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C']
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': [10, 20, 30]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['invalid_type'],
            title='Invalid Type'
        )
        
        assert response['status'] == 'ERROR'
        assert 'error_type' in response
        assert 'message' in response
    
    def test_missing_columns_key(self):
        """Test error handling when 'columns' key is missing."""
        data = {
            'labels': ['A', 'B', 'C'],
            'values': [10, 20, 30]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Missing Columns'
        )
        
        assert response['status'] == 'ERROR'
        assert 'error_type' in response
        assert 'message' in response
    
    def test_non_dict_data(self):
        """Test error handling for non-dict data."""
        data = "invalid data"
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Non-Dict Data'
        )
        
        assert response['status'] == 'ERROR'
        assert 'error_type' in response
        assert 'message' in response


class TestChartPerformance:
    """Test performance aspects of chart generation."""
    
    def test_large_dataset(self):
        """Test chart generation with large dataset."""
        labels = [f'Item {i}' for i in range(100)]
        values = list(range(100))
        
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': labels
                },
                {
                    'name': 'Values',
                    'type': 'number',
                    'examples': values
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['bar'],
            title='Large Dataset'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
    
    def test_multiple_series(self):
        """Test chart with multiple data series."""
        data = {
            'columns': [
                {
                    'name': 'labels',
                    'type': 'string',
                    'examples': ['A', 'B', 'C', 'D']
                },
                {
                    'name': 'Series1',
                    'type': 'number',
                    'examples': [10, 20, 30, 40]
                },
                {
                    'name': 'Series2',
                    'type': 'number',
                    'examples': [40, 30, 20, 10]
                },
                {
                    'name': 'Series3',
                    'type': 'number',
                    'examples': [25, 25, 25, 25]
                }
            ]
        }
        
        response = generate_chartjs(
            data=data,
            chart_types=['line'],
            title='Multiple Series'
        )
        
        assert response['status'] == 'SUCCESS'
        assert 'html_path' in response
