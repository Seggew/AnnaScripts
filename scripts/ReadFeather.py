import pandas as pd

# Replace 'your_file.feather' with the actual path to your Feather file
feather_file = '/Users/seggewa/Desktop/Length/2024-08-23_11-24-03_SV18.predictions.feather'

# Load the Feather file into a pandas DataFrame
df = pd.read_feather(feather_file)

# Print the column names of the DataFrame
print("Column names in the DataFrame:")
print(df.columns)
