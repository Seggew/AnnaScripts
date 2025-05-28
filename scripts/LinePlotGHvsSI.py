# %%
# Improved script to allow Seaborn to compute CI from raw (unaggregated) data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# allows text to be editable in Illustrator
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# font settings
plt.rcParams['font.size'] = 5
plt.rcParams['font.family'] = 'arial'

# Load data
data = pd.read_csv("filtered_combined_clustersSIcontrol.csv")

# %%
# Mark whether the track is in a cluster
data['in_cluster'] = data['cluster'] > -1

# Filter frames and conditions
data = data[(data['frame'] <= 200000)]
data = data[data['condition'].isin(['SI_newSI', 'GH_newGH'])]

# Relabel the conditions
data['condition'] = data['condition'].replace({
    'GH_newGH': 'Group-housed',
    'SI_newSI': 'Social-Isolation'
})

# Compute per-frame, per-file fraction in cluster
fractions_by_file = (
    data.groupby(['origin_file', 'frame'], as_index=False)
    .agg(fraction_in_cluster=('in_cluster', 'mean'))
)

#Merge condition info back
fractions_by_file = fractions_by_file.merge(
    data[['origin_file', 'condition']].drop_duplicates(), on='origin_file'
)


# Bin the frame numbers, but DO NOT aggregate yet
fractions_by_file['frame_bin'] = (fractions_by_file['frame'] // 1500) * 1500 # frame to time conversion first, then binning
fractions_by_file['time_hours'] = fractions_by_file['frame_bin'] / 18000
fractions_by_file = fractions_by_file.groupby(['origin_file','time_hours', 'condition'], as_index=False)['fraction_in_cluster'].mean()

# %%
try:
    color_dict = {
        'Social-Isolation': '#FF8A15',
        'Group-housed': '#52B152'
    }

    plt.figure(figsize=(12, 8))

    sns.lineplot(
        data=fractions_by_file,
        x='time_hours',
        y='fraction_in_cluster',
        hue='condition',
        palette=color_dict,
        #estimator='mean',
        errorbar=("ci",95),
        linewidth=3,
        alpha=0.8
    )

    # Labels and title
    plt.xlabel("Time (in hours)", fontsize=14)
    plt.ylabel("Fraction of Track IDs in Clusters", fontsize=14)
    plt.title("Average Clustering Over Time (CI from raw data)", fontsize=16)
    plt.legend(title="Condition", fontsize=12)
    plt.grid(False)
    plt.tight_layout()

    # Save the plot
    output_plot_path = os.path.join(os.getcwd(), "TimeseriesFraction_Unaggregated.pdf")
    plt.savefig(output_plot_path, dpi=300)
    plt.show()
    plt.close()

    print(f"Plot saved successfully at: {output_plot_path}")

except Exception as e:
    print(f"Error generating or saving plot: {e}")
    exit()

# %%
