from .base import ChartGenerator

class PieChartGenerator(ChartGenerator):
    def __init__(self):
        super().__init__()
        self.chart_type = "pie"

    def _get_type_specific_controls(self):
        return """
        <div class="control-group">
            <label for="showPercentage">Show Percentage:</label>
            <input type="checkbox" id="showPercentage" checked>
        </div>
        <div class="control-group">
            <label for="showLabels">Show Labels:</label>
            <input type="checkbox" id="showLabels" checked>
        </div>
        """

    def _get_type_specific_js(self):
        return """
            const showPercentage = document.getElementById('showPercentage').checked;
            const showLabels = document.getElementById('showLabels').checked;
            
            newConfig.options.plugins.datalabels.formatter = function(value, ctx) {
                let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);
                let percentage = showPercentage ? (value * 100 / sum).toFixed(1) + '%' : '';
                let label = showLabels ? ctx.chart.data.labels[ctx.dataIndex] : '';
                return [label, percentage].filter(Boolean).join(': ');
            };
        """

    def generate(self, data, **options):
        labels = []
        dataset = {}
        
        # Extract labels from first string column
        for col in data['columns']:
            if col['type'] == 'string':
                labels = col['examples']
                break
                
        # Use first numeric column for pie data
        for col in data['columns']:
            if col['type'] == 'number':
                dataset = {
                    'label': col['name'],
                    'data': col['examples'],
                    'backgroundColor': [
                        self.default_colors[i % len(self.default_colors)]
                        for i in range(len(col['examples']))
                    ],
                    'borderColor': '#fff',
                    'borderWidth': 1
                }
                break
        
        config = {
            'type': 'pie',
            'data': {
                'labels': labels,
                'datasets': [dataset]
            },
            'options': {
                'responsive': True,
                'plugins': {
                    'title': {
                        'display': True,
                        'text': options.get('title', 'Pie Chart')
                    },
                    'datalabels': {
                        'formatter': 'function(value, ctx) {\n'
                                     '  let sum = ctx.dataset.data.reduce((a, b) => a + b, 0);\n'
                                     '  let percentage = (value * 100 / sum).toFixed(1) + \'%\'\n'
                                     '  return ctx.chart.data.labels[ctx.dataIndex] + \': \' + percentage;\n'
                                     '}',
                        'color': '#fff'
                    }
                }
            }
        }
        
        return self._save_chart(config, options.get('title', 'Pie Chart'))