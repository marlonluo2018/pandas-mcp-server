import os
from visualization import generate_chartjs as generate_pyecharts

def print_chart_result(result, chart_type):
    if result['status'] == 'SUCCESS':
        print(f"✅ {chart_type} Chart generated successfully")
        print(f"📄 HTML path: {result['html_path']}")
        print(f"🔍 File exists: {os.path.exists(result['html_path'])}\n")
    else:
        print(f"❌ Failed to generate {chart_type} chart:")
        print(result['message'])
        if 'traceback' in result:
            print(result['traceback'])

# Test data for pie charts
pie_data = {
    "columns": [
        {"name": "Category", "type": "string", "examples": ["Food", "Travel", "Shopping", "Entertainment"]},
        {"name": "Expense", "type": "number", "examples": [500, 300, 200, 400]},
         ]
}

# Test data for bar charts
bar_data = {
    "columns": [
        {"name": "Month", "type": "string", "examples": ["Jan", "Feb", "Mar", "Apr"]},
        {"name": "Revenue", "type": "number", "examples": [150, 240, 350, 480]},
        {"name": "Cost", "type": "number", "examples": [100, 180, 250, 320]}
    ]
}

# Test data for line charts
line_data = {
    "columns": [
        {"name": "Quarter", "type": "string", "examples": ["Q1", "Q2", "Q3", "Q4"]},
        {"name": "Profit", "type": "number", "examples": [50, 120, 180, 210]},
        {"name": "Revenue", "type": "number", "examples": [200, 350, 480, 600]}
    ]
}

# Generate and test charts
print("Testing chart generation...\n")

# Test pie chart
pie_result = generate_pyecharts(
    pie_data,
    chart_types=["pie"],
    title="Expense Analysis"
)
print_chart_result(pie_result, "Pie")

# Test bar chart
bar_result = generate_pyecharts(
    bar_data,
    chart_types=["bar"],
    title="Monthly Revenue vs Cost"
)
print_chart_result(bar_result, "Bar")

# Test line chart
line_result = generate_pyecharts(
    line_data,
    chart_types=["line"],
    title="Quarterly Profit & Revenue"
)
print_chart_result(line_result, "Line")

print("✅ All charts generated successfully")