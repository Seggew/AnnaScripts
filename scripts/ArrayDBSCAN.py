import pandas as pd
from sklearn.cluster import DBSCAN
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import sys

# Define the input and output directories
input_dir = os.getcwd()  # Assumes the script is dropped in the folder with Feather files
output_dir = os.path.join(input_dir, "DBSCANarray")
os.makedirs(output_dir, exist_ok=True)

# Get the list of all Feather files
feather_files = [f for f in os.listdir(input_dir) if f.endswith(".feather")]

# Obtain the job array index (assuming it's passed as an environment variable)
# In SLURM, this would be $SLURM_ARRAY_TASK_ID; adjust for your environment if necessary
try:
    array_index = int(os.getenv("SLURM_ARRAY_TASK_ID", 0))
except (TypeError, ValueError):
    print("Error: Array index not found or invalid.")
    sys.exit(1)

# Check if the array index is within the range of available files
if array_index < 0 or array_index >= len(feather_files):
    print(f"Error: Array index {array_index} is out of bounds.")
    sys.exit(1)

# Select the Feather file corresponding to the current array index
filename = feather_files[array_index]
data_path = os.path.join(input_dir, filename)

# Load the dataset from the feather file
data = pd.read_feather(data_path)

# Filter data for every 10th frame
filtered_data = data[(data['frame'] % 10 == 0)]

# Select the relevant columns for DBSCAN (head and tail coordinates)
coordinates = filtered_data[['track_id', 'frame', 'x_head', 'y_head', 'x_tail', 'y_tail']].dropna()

# Calculate vectors for each instance (tail - head)
coordinates['vector_x'] = coordinates['x_tail'] - coordinates['x_head']
coordinates['vector_y'] = coordinates['y_tail'] - coordinates['y_head']

# Define the custom distance function with separate checks
def custom_distance(A, B):
    tail_A = A[:2]  # x_tail and y_tail of A
    tail_B = B[:2]  # x_tail and y_tail of B
    euclidean_tail_dist = np.linalg.norm(tail_A - tail_B)
    
    vector_A = A[2:]  # vector_x and vector_y of A
    vector_B = B[2:]  # vector_x and vector_y of B
    magnitude_A = np.linalg.norm(vector_A)
    magnitude_B = np.linalg.norm(vector_B)
    
    if magnitude_A == 0 or magnitude_B == 0:
        return 1000
    
    cos_similarity = np.dot(vector_A, vector_B) / (magnitude_A * magnitude_B)
    
    if cos_similarity > 0.9:
        return euclidean_tail_dist
    
    return 1000

# Initialize an empty list to store clustering results
clustering_results = []

# Loop through each frame for separate clustering and plotting
for frame, group in coordinates.groupby('frame'):
    data_for_clustering = group[['x_tail', 'y_tail', 'vector_x', 'vector_y']].values
    
    # Apply DBSCAN with the custom metric
    dbscan = DBSCAN(eps=45, min_samples=3, metric=lambda A, B: custom_distance(A, B))
    labels = dbscan.fit_predict(data_for_clustering)
    
    group['cluster'] = labels
    clustering_results.append(group)
    
    # Plot the results for the current frame
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=group['x_tail'], y=group['y_tail'], hue=group['cluster'], palette='viridis', s=50)
    plt.title(f'Frame {frame} - customDBSCAN Clustering')
    plt.xlabel('x_tail')
    plt.ylabel('y_tail')
    
    # Save the plot
    plot_filename = f"{os.path.splitext(filename)[0]}_frame_{frame}_dbscan.png"
    plot_path = os.path.join(output_dir, plot_filename)
    plt.savefig(plot_path)
    plt.close()

# Concatenate all frame clustering results into a single DataFrame
result_df = pd.concat(clustering_results, ignore_index=True)

# Save clustering results to CSV
csv_filename = f"{os.path.splitext(filename)[0]}_CustomDBSCANeps=45-cos=.9.csv"
csv_path = os.path.join(output_dir, csv_filename)
result_df.to_csv(csv_path, index=False)

print(f"Processed {filename}: Clustering results and plots saved.")
