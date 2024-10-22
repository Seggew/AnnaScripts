import os
import pandas as pd
import numpy as np
import seaborn as sns
#%matplotlib inline
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import networkx as nx


df = pd.read_csv('/Users/seggewa/Desktop/DataAnalysis/2024-02-05_all-labels_tracks.v007.000_2023_11_13_white_ON_1800,1100_totalpixels-1980000_new.analysis.csv')


# Calculate distances (ensure this matches the structure of your DataFrame)
distance_data = []
for frame in df['frame_idx'].unique():
    unique_frame = df[df['frame_idx'] == frame]
    body_coordinates = unique_frame[['spiracle.x', 'spiracle.y']].to_numpy()
    distance_matrix = cdist(body_coordinates, body_coordinates, 'euclidean')
    np.fill_diagonal(distance_matrix, np.nan)

    for i in range(distance_matrix.shape[0]):
        for j in range(i + 1, distance_matrix.shape[1]):
            distance_pixels = distance_matrix[i, j]
            if not np.isnan(distance_pixels) and distance_pixels <= 100:
                distance_data.append({
                    'frame_idx': frame,
                    'track_pair': f"{unique_frame.iloc[i]['track']} - {unique_frame.iloc[j]['track']}",
                    'distance_pixels': distance_pixels
                })

df_distances_filtered = pd.DataFrame(distance_data)

# Create a graph for cluster identification
G = nx.Graph()

# Assume each row in df_distances_filtered represents a pair within 100 pixels
for _, row in df_distances_filtered.iterrows():
    track_a, track_b = row['track_pair'].split(' - ')
    G.add_edge(track_a, track_b)

# Identify clusters
clusters = [c for c in nx.connected_components(G) if len(c) >= 3]

# clusters now contains sets of track IDs that form clusters

# Optionally, you can create a DataFrame from the clusters for further analysis or export
clusters_df = pd.DataFrame({'Cluster': list(range(1, len(clusters) + 1)),
                            'Tracks': [', '.join(cluster) for cluster in clusters]})

print(clusters_df)

