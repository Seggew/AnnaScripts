import pandas as pd
import matplotlib.pyplot as plt

# Path to the combined CSV file
csv_file = '/Users/seggewa/Desktop/Length'

# Load the combined CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Group by 'condition' and calculate the mean of 'body_length'
average_body_length = df.groupby('condition')['body_length'].mean()

# Create a bar plot
plt.figure(figsize=(10, 6))
average_body_length.plot(kind='bar')

# Add labels and title
plt.ylabel('Average Body Length')
plt.xlabel('Condition')
plt.title('Average Body Length per Condition')

# Show the plot
plt.tight_layout()
plt.show()
