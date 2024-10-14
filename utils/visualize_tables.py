import re
import pandas as pd
import matplotlib.pyplot as plt

def extract_drawing_info(content):
    pattern = r"row_index=(\d+).*?column_index=0.*?content=([^,]+).*?column_index=1.*?content=([^,]+)"
    matches = re.findall(pattern, content, re.DOTALL)
    
    data = []
    for match in matches:
        row_index, col0, col1 = match
        if col0.strip() and col1.strip() and col0.strip() != 'DWG. NO':
            data.append((col0.strip(), col1.strip()))
    
    return data

# Read the file content
with open('paste.txt', 'r') as file:
    content = file.read()

# Extract drawing information
data = extract_drawing_info(content)

# Create a DataFrame
df = pd.DataFrame(data, columns=['Drawing Number', 'Title'])

# Create a bar chart
plt.figure(figsize=(12, 6))
plt.barh(df['Drawing Number'], range(len(df)), align='center')
plt.yticks(range(len(df)), df['Drawing Number'])

# Add labels to the bars
for i, title in enumerate(df['Title']):
    plt.text(0.1, i, title, va='center')

plt.title('Index of Drawings')
plt.xlabel('Drawing Title')
plt.ylabel('Drawing Number')
plt.tight_layout()

# Save the chart
plt.savefig('drawing_index_chart.png')

# Display the chart (if running in an interactive environment)
plt.show()

# Print the DataFrame for a tabular view
print(df)