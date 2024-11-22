import pandas as pd
from sklearn.cluster import DBSCAN
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

# Load the dataset from the feather file
data = pd.read_feather("/Users/seggewa/Desktop/cluster/1hrTRIM2024-08-29_14-01-33_SV2.tracks.feather")

# Filter data for frames 1 to 3
filtered_data = data[(data['frame'] % 10 == 0)]

# Select the relevant columns for DBSCAN (head and tail coordinates)
coordinates = filtered_data[['track_id', 'frame', 'x_head', 'y_head', 'x_tail', 'y_tail']]

# Drop rows with missing values in head or tail coordinates
coordinates = coordinates.dropna(subset=['x_head', 'y_head', 'x_tail', 'y_tail'])

# Calculate vectors for each instance (tail - head)
coordinates['vector_x'] = coordinates['x_tail'] - coordinates['x_head']
coordinates['vector_y'] = coordinates['y_tail'] - coordinates['y_head']

# Define the custom distance function with separate checks
def custom_distance(A, B):
    # A and B are expected to contain the [x_tail, y_tail, vector_x, vector_y] of each point
    
    # Step 1: Calculate Euclidean distance between tail coordinates
    tail_A = A[:2]  # x_tail and y_tail of A
    tail_B = B[:2]  # x_tail and y_tail of B
    euclidean_tail_dist = np.linalg.norm(tail_A - tail_B)
    
    # Step 2: Calculate cosine similarity based on the vectors (vector_x, vector_y)
    vector_A = A[2:]  # vector_x and vector_y of A
    vector_B = B[2:]  # vector_x and vector_y of B
    magnitude_A = np.linalg.norm(vector_A)
    magnitude_B = np.linalg.norm(vector_B)
    
    # Avoid division by zero for vectors with zero magnitude
    if magnitude_A == 0 or magnitude_B == 0:
        return 1000  # Treat zero-magnitude vectors as far apart
    
    cos_similarity = np.dot(vector_A, vector_B) / (magnitude_A * magnitude_B)
    
    # Step 3: Check both conditions
    # Condition 1: Euclidean distance between tail coordinates must be within 50
    # Condition 2: Cosine similarity must be positive (angle < 90 degrees)
    if cos_similarity > 0.9:
        return euclidean_tail_dist  # Return the actual tail distance if both conditions are met
    
    return 1000  # Large distance if either condition fails

# Initialize an empty list to store clustering results
clustering_results = []

# Directory to save the plots
output_dir = "/Users/seggewa/Desktop/gridsearch/EXPERIMENT"
os.makedirs(output_dir, exist_ok=True)

# Loop through each frame for separate clustering and plotting
for frame, group in coordinates.groupby('frame'):
    # Prepare data for custom metric with [x_tail, y_tail, vector_x, vector_y]
    data_for_clustering = group[['x_tail', 'y_tail', 'vector_x', 'vector_y']].values
    
    # Apply DBSCAN with the custom metric
    dbscan = DBSCAN(eps=45, min_samples=3, metric=lambda A, B: custom_distance(A, B))
    labels = dbscan.fit_predict(data_for_clustering)
    
    # Add clustering results to the group data
    group['cluster'] = labels
    
    # Append the labeled data for this frame to the main list
    clustering_results.append(group)
    
    # Plot the results for the current frame
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=group['x_tail'], y=group['y_tail'], hue=group['cluster'], palette='viridis', s=50)
    plt.title(f'Frame {frame} - customDBSCAN Clustering')
    plt.xlabel('x_tail')
    plt.ylabel('y_tail')
    
    # Save the plot
    plot_path = os.path.join(output_dir, f'frame_{frame}_dbscan.png')
    plt.savefig(plot_path)
    plt.close()

# Concatenate all frame clustering results into a single DataFrame
result_df = pd.concat(clustering_results, ignore_index=True)

# Save clustering results to CSV
result_df.to_csv("CustomDBSCANeps=45-cos=.9.csv", index=False)
print("Clustering results and plots saved.")
