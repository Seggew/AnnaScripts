import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

#test line for git
master_csv_path = '/Users/seggewa/Desktop/Cass/ClusterInfo_20241022.csv'
data = pd.read_csv(master_csv_path)

data['Condition_numeric'] = pd.to_numeric(data['Condition'], errors='coerce')
data = data.sort_values(by='Condition_numeric')

# ANOVA
grouped_percentage = data.groupby('Condition')['Average-Percentage']
grouped_clusters = data.groupby('Condition')['Clusters']

#Plotting
conditions = data['Condition'].unique() 
average_percentages = [grouped_percentage.get_group(cond).mean() for cond in conditions]
total_clusters = [grouped_clusters.get_group(cond).mean() for cond in conditions]

# Define figure size and create subplots. absolute bar positions and width
fig, ax = plt.subplots(figsize=(5, 4))
positions = np.arange(len(conditions)) 
bar_width = 0.35
colors_percentage = '#30694F'
colors_clusters = '#B8CCC3'

#bar plotting
percentage_bars = ax.bar(positions - bar_width/2, average_percentages, bar_width, label='Average Percentage', color=colors_percentage)
clusters_bars = ax.bar(positions + bar_width/2, total_clusters, bar_width, label='Total Clusters', color=colors_clusters)


# Add individual data points
for i, cond in enumerate(conditions):
    individual_percentages = grouped_percentage.get_group(cond)
    ax.scatter(
        np.full(len(individual_percentages), positions[i] - bar_width/2),
        individual_percentages,
        facecolors='none', edgecolors='black', s=40, zorder=2, linewidth=0.8
    )

    individual_clusters = grouped_clusters.get_group(cond)
    ax.scatter(
        np.full(len(individual_clusters), positions[i] + bar_width/2),
        individual_clusters,
        facecolors='none', edgecolors='black', s=30, zorder=2, linewidth=0.8
    )


ax.set_xlabel('Conditions')
ax.set_ylabel('Values')
ax.set_xticks(positions)
ax.set_xticklabels(conditions, rotation=45, ha="right")  # Rotate the labels for better visibility if necessary
ax.legend()

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()  
plt.show()
