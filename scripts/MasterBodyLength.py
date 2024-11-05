
import os
import pandas as pd

# Folder A (replace with the actual path to your folder A)
folder_a = '/Users/seggewa/Desktop/Length100000'

# List to store all the combined data
combined_data = []

# Loop through each subfolder in folder A
for subfolder in os.listdir(folder_a):
    subfolder_path = os.path.join(folder_a, subfolder)

    # Check if the subfolder path is indeed a directory (not a file)
    if os.path.isdir(subfolder_path):
        # Look for the CSV file inside the subfolder
        csv_file_path = os.path.join(subfolder_path, '400klarva_body_lengths.csv')

        # If the CSV file exists in the subfolder, process it
        if os.path.exists(csv_file_path):
            # Read the CSV file into a DataFrame
            df = pd.read_csv(csv_file_path)

            # Add a new 'condition' column with the subfolder name
            df['condition'] = subfolder

            # Append the DataFrame to the list
            combined_data.append(df)

# Combine all the DataFrames into one large DataFrame
final_combined_df = pd.concat(combined_data, ignore_index=True)

# Save the final combined DataFrame to a CSV file in folder A
output_path = os.path.join(folder_a, '400kcombined_larva_data.csv')
final_combined_df.to_csv(output_path, index=False)

print(f"Combined data saved to '{output_path}'")
