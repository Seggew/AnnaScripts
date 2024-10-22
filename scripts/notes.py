import os
import pandas as pd

# Change directory to where the data file is located
os.chdir('/Users/seggewa/Desktop/FeatherAnalysis/0.8mm')  # Replace with the correct path

# Now, load your data file (e.g., CSV, Excel, etc.)
df = pd.read_csv('/Users/seggewa/Desktop/FeatherAnalysis/0.8mm/ClusterAnalysis_2023-12-31_03-02-34_SV12.predictions.csv')  # Replace 'your_file.csv' with the actual file name

# Print the column names
print(df.columns)
