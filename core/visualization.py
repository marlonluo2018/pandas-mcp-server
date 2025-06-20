from .chart_generators import BarChartGenerator, PieChartGenerator, LineChartGenerator
import os
import traceback
from .config import CHARTS_DIR
from urllib.parse import parse_qs

def generate_chartjs(
    data: dict,
    chart_types: list = None,
    title: str = "Data Visualization",
    request_params: dict = None,
) -> dict:
    """Generate interactive Chart.js visualizations from structured data."""
    try:
        if not isinstance(data, dict) or 'columns' not in data:
            return {
                "status": "ERROR",
                "message": "Invalid data format"
            }

        if not chart_types:
            return {
                "status": "ERROR",
                "message": "Must specify chart types"
            }

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
            return {
                "status": "ERROR",
                "message": f"Invalid chart type '{chart_type}'"
            }

        # Ensure title is passed properly
        options['title'] = str(title) if title else "Chart"

        # Debug logging
        print(f"DEBUG - Data structure: {data}")
        print(f"DEBUG - Columns type: {type(data['columns'])}")
        if data['columns']:
            print(f"DEBUG - First column type: {type(data['columns'][0])}")

        result = generator.generate(data)
        return result

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e),
            "traceback": traceback.format_exc()
        }