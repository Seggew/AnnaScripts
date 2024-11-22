import pandas as pd
from sklearn.cluster import DBSCAN
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the dataset from the feather file
data = pd.read_feather("/Users/seggewa/Desktop/cluster/1hrTRIM2024-08-29_14-01-33_SV2.tracks.feather")

# Filter data for frames 1 to 10
filtered_data = data[(data['frame'] >= 1) & (data['frame'] <= 1)]

# Select the relevant columns for DBSCAN (tail coordinates)
coordinates = filtered_data[['track_id', 'frame', 'x_tail', 'y_tail']]

# Drop rows with missing values in x_tail or y_tail
coordinates = coordinates.dropna(subset=['x_tail', 'y_tail'])

# Initialize an empty list to store clustering results
clustering_results = []

# Directory to save the plots
output_dir = "/Users/seggewa/Desktop/trim/DBSCAN_plots"
os.makedirs(output_dir, exist_ok=True)

# Loop through each frame for separate clustering and plotting
for frame, group in coordinates.groupby('frame'):
    # Extract the tail coordinates for the frame
    tail_coords = group[['x_tail', 'y_tail']]
    
    # Apply DBSCAN on tail coordinates
    dbscan = DBSCAN(eps=45, min_samples=2)  # Adjust eps and min_samples as needed
    labels = dbscan.fit_predict(tail_coords)
    
    # Add clustering results to the group data
    group['cluster'] = labels
    
    # Append the labeled data for this frame to the main list
    clustering_results.append(group)


# Concatenate all frame clustering results into a single DataFrame
result_df = pd.concat(clustering_results, ignore_index=True)

# Save clustering results to CSV
result_df.to_csv("/Users/seggewa/Desktop/gridsearch/UglyExample.csv", index=False)
print("Clustering results and plots saved.")
