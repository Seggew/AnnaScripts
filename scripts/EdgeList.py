import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform

# Load the dataset from the feather file using pandas
data = pd.read_feather("/Users/seggewa/Desktop/cluster/1hrTRIM2024-08-29_14-01-33_SV2.tracks.feather")

filtered_data = data[(data['frame'] >= 1) & (data['frame'] <= 10)]
# Initialize an empty list to store distance data
distance_data = []

# Loop through each frame in the dataset
for frame, group in data.groupby('frame'):
    # Extract tail coordinates for all track_ids in the frame
    coords = group[['track_id', 'x_tail', 'y_tail']].set_index('track_id')
    
    # Compute pairwise Euclidean distances
    distances = pd.DataFrame(
        squareform(pdist(coords, metric='euclidean')),
        index=coords.index,
        columns=coords.index
    )
    
    # Melt the distance DataFrame to have track_id pairs and distances in long format
    distances = distances.reset_index().melt(id_vars='track_id', var_name='other_track_id', value_name='tail_distance')
    
    # Add frame information to each row
    distances['frame'] = frame
    
    # Append the distances to the main list
    distance_data.append(distances)

# Concatenate all frame distance data into a single DataFrame
result_df = pd.concat(distance_data, ignore_index=True)

# Save the result to a CSV file
result_df.to_csv("/Users/seggewa/Desktop/cluster/1-10Edgelist.csv", index=False)

print("Distance calculations saved to '1-10Edgelist.csv'")
