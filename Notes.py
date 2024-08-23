import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Assuming data loading and initial processing are done correctly
data = pd.read_csv('/Users/seggewa/Desktop/FeatherAnalysis/ClusterInfo_20240731.csv')

# Calculate the average of the percentage columns for each condition
data['Average-Percentage'] = data[['Inputfiles0.7mm', 'InputfilesIsolation']].mean(axis=1)

# Standardize the AvgPercentage values
data['StandardizedAvgPercentage'] = (data['Average-Percentage'] - data['Average-Percentage'].mean()) / data['Average-Percentage'].std()

# Columns to process for statistical analysis
percent_rows = ['Inputfiles0.7mm', 'InputfilesIsolation']

# Calculate the mean and standard error of the standardized average percentage column grouped by the 'condition' row
means = data.groupby('Condition')['StandardizedAvgPercentage'].mean()
errors = data.groupby('Condition')['StandardizedAvgPercentage'].sem()

# Function to plot bar charts for the averages of the specified conditions with error bars
def plot_comparison():
    # Define labels for the conditions
    condition_mapping = {
        'Inputfiles0.7mm': '0.7mm', 
        'InputfilesIsolation': 'Isolated'
    }

    # Select the data for 'StandardizedAvgPercentage'
    groups_data = means.loc[['Inputfiles0.7mm', 'InputfilesIsolation']]
    group_errors = errors.loc[['Inputfiles0.7mm', 'InputfilesIsolation']]

    # Perform a t-test between the two groups with standardized values
    PointSeven = data[data['Condition'] == 'Inputfiles0.7mm']['StandardizedAvgPercentage']
    Isolation = data[data['Condition'] == 'InputfilesIsolation']['StandardizedAvgPercentage']
    
    t_stat_37, p_value_37 = stats.ttest_ind(PointSeven, Isolation)

    # Determine significance level
    def get_significance(p_value):
        if p_value < 0.001:
            return '***'
        elif p_value < 0.01:
            return '**'
        elif p_value < 0.05:
            return '*'
        else:
            return 'ns'  # Not significant

    significance_37 = get_significance(p_value_37)

    # Define figure size
    fig, ax = plt.subplots(figsize=(2.8, 4))  # Adjusted width for two bars

    # Define absolute bar positions and width
    positions = [0.3, 0.7]  # Absolute positions for each bar on the x-axis
    bar_width = 0.3  # Absolute bar width

    # Colors for each group
    colors = ['#30694F', '#B8CCC3']  # Specific colors for each condition

    # Plot bars at specified positions
    max_height = 0
    for pos, cond, color in zip(positions, [3, 7], colors):
        bar = ax.bar(pos, groups_data.loc[cond], bar_width, color=color, yerr=group_errors.loc[cond], capsize=4)
        max_height = max(max_height, bar[0].get_height() + group_errors.loc[cond])

    # Set axis labels and title
    ax.set_xlabel('Conditions')
    ax.set_ylabel('Standardized Fraction of clustering larvae')
 
    ax.set_xticks(positions)
    ax.set_xticklabels([condition_mapping[cond] for cond in [3, 7]])

    # Add significance line and annotation if there is significance
    y_max = max_height + 0.1  # Adjust height for the line

    if significance_37 != 'ns':
        ax.plot([positions[0], positions[1]], [y_max, y_max], color='black')
        ax.text((positions[0] + positions[1]) / 2, y_max + 0.02, significance_37, ha='center')

    # Remove the top and right spines (outer frame) while keeping the x and y axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()

# Call the function to plot
plot_comparison()
