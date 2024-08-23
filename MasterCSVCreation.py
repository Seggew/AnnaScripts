import os
import pandas as pd
from datetime import datetime

# Define the main directory containing the subfolders
main_dir = '/Users/seggewa/Desktop/FeatherAnalysis'

# Prepare a DataFrame to hold all the collected data
master_data = pd.DataFrame()

# Traverse through each subfolder
for condition in os.listdir(main_dir):
    subfolder_path = os.path.join(main_dir, condition)
    if os.path.isdir(subfolder_path):  # Check if it is a directory
        # Process each file in the subfolder
        for trial in os.listdir(subfolder_path):
            if trial.endswith('.csv'):
                file_path = os.path.join(subfolder_path, trial)
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Calculate total number of clusters
                total_clusters = len(df['Cluster'].unique())

                # Calculate average percentage of tracks in clusters
                average_percentage = df['Percentage of Tracks in Clusters'].mean()

                # Create a DataFrame for the current file's data
                temp_df = pd.DataFrame({
                    'Condition': [condition],
                    'Trial': [trial],
                    'Clusters': [total_clusters],
                    'Average-Percentage': [average_percentage]
                })

                # Append the data to the master DataFrame using concat
                master_data = pd.concat([master_data, temp_df], ignore_index=True)

# Get the current date in YYYYMMDD format
current_date = datetime.now().strftime('%Y%m%d')

# Specify the path for the output master CSV file
output_csv_path = os.path.join(main_dir, f'ClusterInfo_{current_date}.csv')

# Save the master DataFrame to CSV
master_data.to_csv(output_csv_path, index=False)

print(f"Master data saved to CSV: {output_csv_path}")
