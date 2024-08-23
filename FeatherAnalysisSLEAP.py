import os
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import networkx as nx
from datetime import datetime

# Load your DataFrame
input_dir = '/Users/seggewa/Desktop/FeatherAnalysis/0.8mm'
for file in os.listdir(input_dir):
    if file.endswith(".feather"):
        original_feather_path = os.path.join(input_dir, file)
        df = pd.read_feather(original_feather_path)

        all_frames_clusters = pd.DataFrame()

        for frame in df['frame'].unique():
            # Filter data for the current frame
            frame_data = df[df['frame'] == frame]
            total_tracks_in_frame = frame_data['track_id'].nunique()
            G = nx.Graph()

            # Calculate distances and filter within 100 pixels
            body_coordinates = frame_data[['x_spiracle', 'y_spiracle']].to_numpy()
            distance_matrix = cdist(body_coordinates, body_coordinates, 'euclidean')
            np.fill_diagonal(distance_matrix, np.nan)

            # Add edges if distance is 10 pixels or less
            for i in range(distance_matrix.shape[0]):
                for j in range(i + 1, distance_matrix.shape[1]):
                    if not np.isnan(distance_matrix[i, j]) and distance_matrix[i, j] <= 10:
                        G.add_edge(frame_data.iloc[i]['track_id'], frame_data.iloc[j]['track_id'])

            # Identify clusters
            clusters = [c for c in nx.connected_components(G) if len(c) >= 5]

            # Calculate the percentage of tracks involved in clusters
            if clusters:
                clustered_tracks = len(set.union(*[set(cluster) for cluster in clusters]))
                cluster_percentage = (clustered_tracks / total_tracks_in_frame) * 100
            else:
                cluster_percentage = 0

            # Create a DataFrame for the current frame's clusters
            frame_clusters = pd.DataFrame({
                'Frame': frame,
                'Cluster': list(range(1, len(clusters) + 1)),
                'Tracks': [', '.join(map(str, cluster)) for cluster in clusters],
                'Percentage of Tracks in Clusters': [cluster_percentage] * len(clusters)
            })

            # Append the current frame's clusters to the all_frames_clusters DataFrame
            all_frames_clusters = pd.concat([all_frames_clusters, frame_clusters], ignore_index=True)

        # Specify the output file name, including "ClusterAnalysis" with the basename of the input file
        output_path = os.path.join(input_dir, f'ClusterAnalysis_{os.path.splitext(file)[0]}.csv')

        # Save the clusters DataFrame to the new CSV file
        all_frames_clusters.to_csv(output_path, index=False)

        print(f"Clusters saved to CSV: {output_path}")
