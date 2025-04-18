from server import bar_chart_to_html, line_chart_to_html, pie_chart_to_html
import time

# Test bar chart
bar_result = bar_chart_to_html(
    categories=['Apples', 'Oranges', 'Bananas', 'Grapes'],
    values=[120, 85, 95, 60],
    title="Fruit Sales"
)
print("Bar chart generated at:", bar_result['filepath'])

# Wait 2 seconds to ensure different timestamp
time.sleep(2)

# Test line chart
line_result = line_chart_to_html(
    labels=['Jan', 'Feb', 'Mar'],
    datasets=[
        {'label': 'Temperature', 'data': [15, 18, 20]},
        {'label': 'Rainfall', 'data': [50, 30, 40]}
    ],
    title="Weather Data"
)
print("Line chart generated at:", line_result['filepath'])

# Wait 2 seconds to ensure different timestamp
time.sleep(2)

# Test pie chart
pie_result = pie_chart_to_html(
    labels=['Windows', 'MacOS', 'Linux'],
    values=[75, 20, 5],
    title="Operating System Market Share"
)
print("Pie chart generated at:", pie_result['filepath'])
