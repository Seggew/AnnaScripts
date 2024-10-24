import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ttest_ind
from datetime import datetime
import itertools

date = datetime.today().strftime('%Y-%m-%d')

# Path to the combined CSV file
csv_file = 'data/Bodylength/combined_larva_data.csv'

# Load the combined CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Group by 'condition' and calculate the mean and standard error of 'body_length'
grouped = df.groupby('condition')['body_length']
average_body_length = grouped.mean()
std_error = grouped.sem()

# Perform pairwise t-tests between conditions
conditions = df['condition'].unique()
p_values = {}

# Get all pairs of conditions
for cond1, cond2 in itertools.combinations(conditions, 2):
    data1 = df[df['condition'] == cond1]['body_length']
    data2 = df[df['condition'] == cond2]['body_length']
    t_stat, p_value = ttest_ind(data1, data2)
    p_values[(cond1, cond2)] = p_value

# Create a bar plot with error bars and set the bar color
plt.figure(figsize=(10, 6))
bars = average_body_length.plot(kind='bar', yerr=std_error, capsize=5, color='#30694F')

# Remove the top and right spines (black lines around the plot)
ax = plt.gca()  # Get the current axis
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add labels and title
plt.ylabel('Average Body Length')
plt.xlabel('Condition')
plt.title('Average Body Length per Condition')

# Add significance stars
# Loop through pairs of conditions and add stars for significant p-values
for (cond1, cond2), p_value in p_values.items():
    if p_value < 0.05:  # Use 0.05 as a threshold for significance
        # Get the positions of the bars for cond1 and cond2
        pos1 = np.where(conditions == cond1)[0][0]
        pos2 = np.where(conditions == cond2)[0][0]
        
        # Get the heights of the bars for cond1 and cond2
        y1 = average_body_length[cond1] + std_error[cond1]
        y2 = average_body_length[cond2] + std_error[cond2]
        
        # Add the star above the higher bar
        y_max = max(y1, y2) + 0.05  # Adjust the 0.05 for the space between the bar and the star
        
        # Add a horizontal line between the two bars
        plt.plot([pos1, pos2], [y_max, y_max], color='black')
        
        # Add the significance star
        plt.text((pos1 + pos2) / 2, y_max, '*', ha='center', va='bottom', color='black')

# Show the plot
plt.tight_layout()
plt.savefig(f'plots/{date}_BodyLengthMainCond.png', bbox_inches='tight', dpi=300)
#plt.show()