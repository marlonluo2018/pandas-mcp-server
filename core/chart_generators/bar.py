from .base import ChartGenerator

class BarChartGenerator(ChartGenerator):
    def __init__(self):
        super().__init__()
        self.chart_type = "bar"

    def _get_type_specific_controls(self):
        return """
        <div class="control-group">
            <label for="barWidth">Bar Width:</label>
            <input type="range" id="barWidth" min="0.1" max="1" step="0.1" value="0.8" onchange="updateChart()">
        </div>
        <div class="control-group">
            <label for="yAxisMin">Y-Axis Minimum:</label>
            <input type="number" id="yAxisMin" value="0" onchange="updateChart()">
        </div>
        """

    def _get_type_specific_js(self):
        return """
            newConfig.options.barPercentage = parseFloat(document.getElementById('barWidth').value);
            newConfig.options.scales.y.min = parseFloat(document.getElementById('yAxisMin').value);
        """

    def generate(self, data, **options):
        labels = []
        datasets = []
        
        # Extract labels from first string column
        for col in data['columns']:
            if col['type'] == 'string':
                labels = col['examples']
                break
                
        # Create dataset for each numeric column
        for i, col in enumerate(data['columns']):
            if col['type'] == 'number':
                datasets.append({
                    'label': col['name'],
                    'data': col['examples'],
                    'backgroundColor': self.default_colors[i % len(self.default_colors)],
                    'borderColor': self.default_colors[i % len(self.default_colors)].replace('0.7', '1'),
                    'borderWidth': 1
                })
        
        config = {
            'type': 'bar',
            'data': {
                'labels': labels,
                'datasets': datasets
            },
            'options': {
                'responsive': True,
                'scales': {
                    'y': {
                        'beginAtZero': True
                    }
                },
                'plugins': {
                    'title': {
                        'display': True,
                        'text': options.get('title', 'Bar Chart')
                    },
                    'datalabels': {
                        'anchor': 'end',
                        'align': 'top'
                    }
                },
                'barPercentage': 0.8
            }
        }
        
        return self._save_chart(config, options.get('title', 'Bar Chart'))