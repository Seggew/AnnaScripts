import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import f_oneway
import numpy as np
import os

# Load the master CSV file
master_csv_path = '/Users/seggewa/Desktop/FeatherAnalysis/ClusterInfo_20240731.csv'
data = pd.read_csv(master_csv_path)

# Perform ANOVA separately for each metric if needed and prepare data for plotting
grouped_percentage = data.groupby('Condition')['Average-Percentage']
grouped_clusters = data.groupby('Condition')['Clusters']

# Data for plotting
conditions = data['Condition'].unique()
average_percentages = [grouped_percentage.get_group(cond).mean() for cond in conditions]
total_clusters = [grouped_clusters.get_group(cond).mean() for cond in conditions]

# Define figure size and create subplots
fig, ax = plt.subplots(figsize=(5, 4))

# Define absolute bar positions and width
positions = np.arange(len(conditions))  # Position indexes
bar_width = 0.35  # Absolute bar width

# Colors for each metric
colors_percentage = '#30694F'
colors_clusters = '#B8CCC3'

# Plot bars for each condition
# Bars for average percentage
percentage_bars = ax.bar(positions - bar_width/2, average_percentages, bar_width, label='Average Percentage', color=colors_percentage)

# Bars for total clusters
clusters_bars = ax.bar(positions + bar_width/2, total_clusters, bar_width, label='Total Clusters', color=colors_clusters)

# Customize axis and labels
ax.set_xlabel('Conditions')
ax.set_ylabel('Values')
ax.set_xticks(positions)
ax.set_xticklabels(conditions)
ax.legend()

# Improve plot aesthetics
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.show()