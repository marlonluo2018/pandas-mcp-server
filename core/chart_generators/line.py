from .base import ChartGenerator

class LineChartGenerator(ChartGenerator):
    def __init__(self):
        super().__init__()
        self.chart_type = "line"

    def _get_type_specific_controls(self):
        return """
        <div class="control-group">
            <label for="lineTension">Line Smoothness:</label>
            <input type="range" id="lineTension" min="0" max="1" step="0.1" value="0.4">
        </div>
        <div class="control-group">
            <label for="steppedLine">Stepped Line:</label>
            <input type="checkbox" id="steppedLine">
        </div>
        <div class="control-group">
            <label for="beginAtZero">Start Y at Zero:</label>
            <input type="checkbox" id="beginAtZero" checked>
        </div>
        """

    def _get_type_specific_js(self):
        return """
            newConfig.options.scales.y.beginAtZero = document.getElementById('beginAtZero').checked;
            newConfig.options.elements.line.tension = parseFloat(document.getElementById('lineTension').value);
            newConfig.options.elements.line.stepped = document.getElementById('steppedLine').checked;
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
                    'borderWidth': 2,
                    'tension': 0.4,
                    'fill': False
                })
        
        config = {
            'type': 'line',
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
                        'text': options.get('title', 'Line Chart')
                    },
                    'datalabels': {
                        'anchor': 'end',
                        'align': 'top'
                    }
                },
                'elements': {
                    'line': {
                        'tension': 0.4,
                        'stepped': False
                    }
                }
            }
        }
        
        return self._save_chart(config, options.get('title', 'Line Chart'))