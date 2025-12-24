from .chart_generators import BarChartGenerator, PieChartGenerator, LineChartGenerator
import os
import traceback
from .config import CHARTS_DIR, ENABLE_CHART_GENERATION
from urllib.parse import parse_qs
from .error_handling import ErrorType, handle_exception, log_and_return_error

def generate_chartjs(
    data: dict,
    chart_types: list = None,
    title: str = "Data Visualization",
    request_params: dict = None,
) -> dict:
    """Generate interactive Chart.js visualizations from structured data."""
    try:
        # Check if chart generation is enabled
        if not ENABLE_CHART_GENERATION:
            return log_and_return_error(
                ErrorType.FEATURE_DISABLED,
                "Chart generation is disabled. Set PANDAS_MCP_ENABLE_CHART_GENERATION=true to enable."
            )
        
        if not isinstance(data, dict) or 'columns' not in data:
            return log_and_return_error(
                ErrorType.INVALID_INPUT,
                "Invalid data format: expected dict with 'columns' key"
            )

        if not chart_types:
            return log_and_return_error(
                ErrorType.INVALID_INPUT,
                "Must specify chart types"
            )

        # Parse request parameters if provided
        options = {}
        if request_params:
            if 'yaxis_min' in request_params:
                options['yaxis_min'] = float(request_params['yaxis_min'][0])
            if 'bar_width' in request_params:
                options['bar_width'] = f"{request_params['bar_width'][0]}%"
            if 'disabled_categories' in request_params:
                options['disabled_categories'] = request_params['disabled_categories']

        chart_type = chart_types[0]
        if chart_type == "bar":
            generator = BarChartGenerator()
        elif chart_type == "pie":
            generator = PieChartGenerator()
        elif chart_type == "line":
            generator = LineChartGenerator()
        else:
            return log_and_return_error(
                ErrorType.INVALID_INPUT,
                f"Invalid chart type '{chart_type}'. Must be one of: bar, pie, line"
            )

        # Ensure title is passed properly
        options['title'] = str(title) if title else "Chart"

        result = generator.generate(data, **options)
        return result

    except Exception as e:
        return handle_exception(
            e,
            ErrorType.TOOL_EXECUTION_ERROR,
            "Failed to generate chart visualization"
        )