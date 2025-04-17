import matplotlib.pyplot as plt

# Data
categories = [
    'Hybrid Cloud Management',
    'Hybrid Cloud Transformation',
    'Data & Technology Transformation',
    'Finance & Supply Chain Transformation'
]
learners = [19, 9, 4, 1]

# Create figure and axis with larger size
plt.figure(figsize=(12, 6))

# Create bar plot with thinner bars (width=0.6)
bars = plt.bar(categories, learners, width=0.6, color=['#4C72B0', '#DD8452', '#55A868', '#C44E52'])

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{int(height)}',
             ha='center', va='bottom', fontsize=10)

# Customize the plot
plt.title('Number of Learners by Category', fontsize=14, pad=20)
plt.xlabel('Categories', fontsize=12, labelpad=10)
plt.ylabel('Number of Learners', fontsize=12, labelpad=10)
plt.xticks(rotation=45, ha='right', fontsize=10)  # Rotate x-axis labels
plt.yticks(fontsize=10)

# Remove top and right spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Add grid lines for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()