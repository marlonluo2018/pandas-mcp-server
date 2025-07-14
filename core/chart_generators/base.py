import os
import json
import time
from abc import ABC, abstractmethod

class ChartGenerator(ABC):
    def __init__(self):
        self.chart_type = None
        self.default_colors = [
            'rgba(54, 162, 235, 0.7)',
            'rgba(255, 99, 132, 0.7)',
            'rgba(75, 192, 192, 0.7)'
        ]

    def _save_chart(self, config, title="Chart"):
        # Get absolute path to this script's directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        print(f"DEBUG - Base directory: {base_dir}")
        
        # Ensure charts directory exists
        charts_dir = os.path.join(base_dir, 'charts')
        print(f"DEBUG - Charts directory: {charts_dir}")
        if not os.path.exists(charts_dir):
            os.makedirs(charts_dir)
            
        filename = f"chart_{self.chart_type}_{int(time.time())}.html"
        filepath = os.path.join(charts_dir, filename)
        print(f"DEBUG - Output file path: {filepath}")
        
        # Load template file using absolute path (include 'core' in path)
        template_path = os.path.join(base_dir, 'core', 'chart_generators', 'templates', f'{self.chart_type}_template.html')
        print(f"DEBUG - Template path: {template_path}")
        print(f"DEBUG - Template exists: {os.path.exists(template_path)}")
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found at: {template_path}")
        with open(template_path, 'r', encoding='utf-8') as f:
            html_template = f.read()
            
        # Replace HTML title placeholders
        html_template = html_template.replace(
            '/*HTML_TITLE_PLACEHOLDER*/',
            title if title else "Chart"
        )
        
        # Replace JS title placeholder with properly quoted text
        js_title = f'"{title if title else "Chart"}"'
        html_template = html_template.replace(
            '/*JS_TITLE_PLACEHOLDER*/\'\'/*JS_TITLE_PLACEHOLDER*/',
            js_title
        )
        
        html_template = html_template.replace(
            '/*DATA_PLACEHOLDER*/{}/*DATA_PLACEHOLDER*/',
            json.dumps(config["data"], indent=4)
        )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_template)
            
        return {'status': 'SUCCESS', 'html_path': filepath, 'type': self.chart_type}

    @abstractmethod
    def generate(self, data, **options):
        pass