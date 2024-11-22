import pandas as pd
import matplotlib.pyplot as plt
from natsort import natsorted

# Load the combined CSV
combined_csv_path = "/Users/seggewa/Desktop/Combined_clustersDBSCAN.csv"  # Replace with the path to your combined CSV
df = pd.read_csv(combined_csv_path)

# Filter for frames up to 400,000
df_filtered = df[df['frame'] <= 400000]

# Check if filtered data is empty
if df_filtered.empty:
    print("No data available for frames up to 400,000. Please check your dataset.")
else:
    # Sort the data by condition for consistency
    data_sorted = df_filtered.loc[natsorted(df_filtered.index, key=lambda x: df_filtered['condition'][x])]

    # Calculate the total number of clusters for each track_id within each condition
    cluster_totals = (
        data_sorted.groupby(['condition', 'track_id'])['cluster']
        .nunique()  # Count unique clusters per track_id
        .groupby('condition')
        .sum()  # Sum all unique cluster counts within each condition
        .reset_index()
    )

    # Rename columns for clarity
    cluster_totals.columns = ['condition', 'total_clusters']

    # Calculate the mean and standard deviation of the total cluster count per condition
    cluster_stats = cluster_totals.groupby('condition')['total_clusters'].agg(['mean', 'std']).reset_index()
    cluster_stats.columns = ['condition', 'average_total_clusters', 'std_total_clusters']

    # Check if cluster_stats contains data for plotting
    if cluster_stats.empty:
        print("No cluster data available after grouping by condition. Please check your dataset.")
    else:
        # Plotting the total number of clusters per condition with error bars
        plt.figure(figsize=(10, 6))
        plt.bar(
            cluster_stats['condition'], 
            cluster_stats['average_total_clusters'], 
            yerr=cluster_stats['std_total_clusters'],  # Adding error bars for standard deviation
            color='#B8CCC3', 
            capsize=5
        )
        plt.xlabel('Condition')
        plt.ylabel('Average Total Number of Clusters')
        plt.title('Total Number of Clusters Across First 400k Frames by Condition')
        plt.xticks(rotation=45, ha="right")  # Adjusts for better readability

        # Save the plot
        output_plot_path = '/Users/seggewa/Desktop/DensityClusters.png'
        plt.tight_layout()
        plt.savefig(output_plot_path, bbox_inches='tight', dpi=300)
        print(f"Plot saved successfully at {output_plot_path}")
