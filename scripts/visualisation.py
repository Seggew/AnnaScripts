import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

# Step 1: Load the CSV file
file_path = '/Users/seggewa/Desktop/cluster/30x3-ClusterAnalysis_1hrTRIM2024-08-29_14-01-33_SV2.tracks.csv'  # Update with your actual file path
data = pd.read_csv(file_path)  # Ensure this line is executed before accessing 'data'

# Step 2: Generate colors for clusters
# Use a colormap and assign different shades to clusters
cluster_ids = data['Cluster'].unique()
color_map = plt.colormaps['viridis']  # Updated colormap call
cluster_colors = {cluster: color_map(i / len(cluster_ids)) for i, cluster in enumerate(cluster_ids)}

# Step 3: Define marker styles for different clusters
cluster_markers = {1: 'o', 2: '^', 3: 's'}  # Cluster 1: dot, Cluster 2: triangle, Cluster 3: square

# Step 4: Loop through each frame and plot
output_folder = '/Users/seggewa/Desktop/cluster/30-3frames_png'
os.makedirs(output_folder, exist_ok=True)

for frame in data['Frame'].unique():
    frame_data = data[data['Frame'] == frame]
    
    plt.figure(figsize=(8, 6))
    
    # Step 5: Plot each track with colors and markers based on the cluster
    for cluster in frame_data['Cluster'].unique():
        cluster_data = frame_data[frame_data['Cluster'] == cluster]
        
        # Assign a different shade for each track within the cluster
        norm = mcolors.Normalize(vmin=0, vmax=len(cluster_data))
        cluster_shade = plt.cm.ScalarMappable(cmap='viridis', norm=norm)

        # Use the specified marker for the current cluster
        marker_style = cluster_markers.get(cluster, 'o')  # Default to 'o' if the cluster isn't in the dictionary

        for i, (_, row) in enumerate(cluster_data.iterrows()):
            x, y = row['x_head'], row['y_head']
            # Adding transparency with alpha=0.7 and setting marker style
            plt.scatter(x, y, color=cluster_shade.to_rgba(i), marker=marker_style, alpha=0.7, label=f'Track {row["Track ID"]}' if i == 0 else "")
    
    # Set the axes limits and invert the y-axis to match the requested coordinate system
    plt.xlim(0, 1800)
    plt.ylim(1100, 0)  # Invert y-axis to make 0 at the top
    
    plt.title(f'Frame {frame}')
    plt.xlabel('x_head')
    plt.ylabel('y_head')
    plt.legend()
    
    # Step 6: Save plot as PDF
    output_png = os.path.join(output_folder, f'frame_{frame}.png')
    plt.savefig(output_png, transparent=True, bbox_inches='tight', pad_inches=0)
    plt.close()

print(f"PNGs saved in {output_folder}")