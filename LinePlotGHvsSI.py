#test script to improve ci on the lineplot!
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import scipy.stats as stats

data = pd.read_csv("filtered_combined_clustersSIcontrol.csv")

data['in_cluster'] = data['cluster'] > -1
data = data[(data['frame'] >= 25000) & (data['frame'] <= 200000)]
data = data[data['condition'].isin(['SI_newSI', 'GH_newGH'])]

try:

    # Relabel the conditions
    # data['condition'] = data['condition'].replace({
    #     'GH_newGH': 'Group-housed',
    #     'SI_newSI': 'Social-Isolation'
    # })

    # Compute the fraction of track_ids in clusters for each frame and origin_file
    fractions_by_file = (
        data.groupby(['origin_file', 'frame'], as_index=False)
        .agg(fraction_in_cluster=('in_cluster', 'mean'))
    )

    # Merge back to get the condition information
    fractions_by_file = fractions_by_file.merge(
        data[['origin_file', 'condition']].drop_duplicates(), on='origin_file'
    )

    # Bin frames into 1500-frame intervals
    fractions_by_file['frame_bin'] = (fractions_by_file['frame'] // 1500) * 1500


    grouped = fractions_by_file.groupby(['condition', 'frame_bin'])['fraction_in_cluster']
    aggregated_data = grouped.agg(['mean', 'count', 'std']).reset_index()

    aggregated_data = aggregated_data.sort_values(by=['condition', 'frame_bin'])

except KeyError as e:
    print(f"Error: Missing expected column '{e.args[0]}' in the dataset. Check your CSV structure.")
    exit()
except Exception as e:
    print(f"Error processing data: {e}")
    exit()

try:
    # Define custom color mapping
    color_dict = {
        'Social-Isolation': '#FF8A15',
        'Group-housed': '#52B152'
    }

    # Plotting
    plt.figure(figsize=(12, 8))

    for condition in aggregated_data['condition'].unique():
        subset = aggregated_data[aggregated_data['condition'] == condition]
        sns.lineplot(
            subset['frame_bin'],
            subset['mean'],
            label=condition,
            color=color_dict.get(condition, 'gray'),
            linestyle='-',
            linewidth=3,
            alpha=0.8.
            ci=95
        )


    # Labels and title
    plt.xlabel("Frame (binned every 1500 frames)", fontsize=14)
    plt.ylabel("Fraction of Track IDs in Clusters", fontsize=14)
    plt.title("Average Clustering Over Time (uncontrolled hatching rate)", fontsize=16)
    plt.legend(title="Condition", fontsize=12)
    plt.grid(True)
    plt.tight_layout()

    # Save the plot in the current directory
    output_plot_path = os.path.join(os.getcwd(), "TimeseriesFraction_BinnedBEFOREcontrollingHATCHING.png")
    plt.savefig(output_plot_path, dpi=300)
    plt.close()

    print(f"Plot saved successfully at: {output_plot_path}")

except Exception as e:
    print(f"Error generating or saving plot: {e}")
    exit()
