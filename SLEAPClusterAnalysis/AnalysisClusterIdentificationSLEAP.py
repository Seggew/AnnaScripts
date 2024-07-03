import os
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import networkx as nx
from datetime import datetime

# Load your DataFrame
original_csv_path = '/Users/seggewa/Desktop/DataAnalysis/2024-02-05_all-labels_tracks.v007.000_2023_11_13_white_ON_1800,1100_totalpixels-1980000_new.analysis.csv'  # Replace with your actual CSV file path
df = pd.read_csv(original_csv_path)

all_frames_clusters = pd.DataFrame()

for frame in df['frame_idx'].unique():
    # Filter data for the current frame
    frame_data = df[df['frame_idx'] == frame]
    total_tracks_in_frame = df[df['frame_idx'] == frame]['track'].nunique()
    G = nx.Graph()

    # Calculate distances and filter within 100 pixels
    body_coordinates = frame_data[['spiracle.x', 'spiracle.y']].to_numpy()
    distance_matrix = cdist(body_coordinates, body_coordinates, 'euclidean')
    np.fill_diagonal(distance_matrix, np.nan)

    # Add edges if distance is 100 pixels or less
    for i in range(distance_matrix.shape[0]):
        for j in range(i + 1, distance_matrix.shape[1]):
            if not np.isnan(distance_matrix[i, j]) and distance_matrix[i, j] <= 50:
                G.add_edge(frame_data.iloc[i]['track'], frame_data.iloc[j]['track'])

    # Identify clusters
    clusters = [c for c in nx.connected_components(G) if len(c) >= 3]

    # Calculate the percentage of tracks involved in clusters
    if clusters:  # Check if there are any clusters
        clustered_tracks = len(set.union(*[set(cluster) for cluster in clusters]))  # Convert each cluster to a set before union
        cluster_percentage = (clustered_tracks / total_tracks_in_frame) * 100
    else:
        cluster_percentage = 0  # No clusters, so the percentage is zero

    # Create a DataFrame for the current frame's clusters
    frame_clusters = pd.DataFrame({
        'Frame': frame,
        'Cluster': list(range(1, len(clusters) + 1)),
        'Tracks': [', '.join(map(str, cluster)) for cluster in clusters],
        'Percentage of Tracks in Clusters': [cluster_percentage] * len(clusters)  # Replicate the percentage for each cluster row
    })

    # Append the current frame's clusters to the all_frames_clusters DataFrame
    all_frames_clusters = pd.concat([all_frames_clusters, frame_clusters], ignore_index=True)

# Specify the output file name, including "ClusterAnalysis" with the basename of the input file
output_path = f'/Users/seggewa/Desktop/DataAnalysis/ClusterAnalysis_{os.path.basename(original_csv_path)}'

# Save the clusters DataFrame to the new CSV file
all_frames_clusters.to_csv(output_path, index=False)

print(f"Clusters saved to CSV: {output_path}")
