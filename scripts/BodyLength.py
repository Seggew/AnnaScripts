import pandas as pd
import numpy as np
import os

# Function to calculate Euclidean distance between two points (x1, y1) and (x2, y2)
def euclidean_distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Folder path containing Feather files (replace with your folder path)
folder_path = '/Users/seggewa/Desktop/Length/isolated'

# List to store results
results = []

# Loop through all Feather files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.feather'):
        # Full path to the current Feather file
        file_path = os.path.join(folder_path, filename)
        
        # Load the Feather file into a pandas DataFrame
        df = pd.read_feather(file_path)
        
        # Filter for rows where frame == 100
        df_filtered = df[df['frame'] == 100000]

        # Calculate Euclidean distances and sum them for each larva
        df_filtered['body_length'] = (
            euclidean_distance(df_filtered['x_head'], df_filtered['y_head'], df_filtered['x_mouthhooks'], df_filtered['y_mouthhooks']) +
            euclidean_distance(df_filtered['x_mouthhooks'], df_filtered['y_mouthhooks'], df_filtered['x_body'], df_filtered['y_body']) +
            euclidean_distance(df_filtered['x_body'], df_filtered['y_body'], df_filtered['x_tail'], df_filtered['y_tail']) +
            euclidean_distance(df_filtered['x_tail'], df_filtered['y_tail'], df_filtered['x_spiracle'], df_filtered['y_spiracle'])
        )

        # Add the results to the list
        for index, row in df_filtered.iterrows():
            results.append({
                'track_id': row['track_id'],
                'feather': filename,
                'body_length': row['body_length']
            })

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a CSV file in the same folder
output_path = os.path.join(folder_path, 'larva_body_lengths.csv')
results_df.to_csv(output_path, index=False)

print(f"Results saved to '{output_path}'")