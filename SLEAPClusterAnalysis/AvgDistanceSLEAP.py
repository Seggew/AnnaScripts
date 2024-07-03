import os
import pandas as pd
import numpy as np
import seaborn as sns
#%matplotlib inline
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# Load the data
df = pd.read_csv('/Users/seggewa/Desktop/DataAnalysis/2024-02-05_all-labels_tracks.v007.000_2023_11_13_white_ON_1800,1100_totalpixels-1980000_new.analysis.csv')

# Initialize a list to hold the distance data
distance_data = []

# Iterate over each unique frame
for frame in df['frame_idx'].unique():
    unique_frame = df[df['frame_idx'] == frame]  # filter to ensure the frame is unique
    
    # Extract body coordinates
    body_coordinates = unique_frame[['spiracle.x', 'spiracle.y']].to_numpy()
    
    # Compute the distance matrix
    distance_matrix = cdist(body_coordinates, body_coordinates, 'euclidean')
    
    # Fill the diagonal with NaN to ignore self-distances
    np.fill_diagonal(distance_matrix, np.nan)
    
    # Conversion factor from pixels to cm
    pixel_to_cm = 6.3 / 1500
    
    # Apply the conversion to each distance
    distance_matrix *= pixel_to_cm
    
    # Iterate over the upper triangle of the distance matrix to avoid duplicate pairs
    for i in range(distance_matrix.shape[0]):
        for j in range(i + 1, distance_matrix.shape[1]):
            if not np.isnan(distance_matrix[i, j]):
                distance_data.append({
                    'frame_idx': frame,
                    'track_pair': f"{unique_frame.iloc[i]['track']} - {unique_frame.iloc[j]['track']}",
                    'distance': distance_matrix[i, j]
                })

# Convert the list of distances into a DataFrame
df_distances = pd.DataFrame(distance_data)

df_distances
print(df_distances)