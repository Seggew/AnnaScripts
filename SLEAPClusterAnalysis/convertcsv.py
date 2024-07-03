import pandas as pd

# Load your CSV file
csv_file_path = '/Users/seggewa/Desktop/DataAnalysis/2024-02-05_all-labels_tracks.v007.000_2023_11_13_white_ON_1800,1100_totalpixels-1980000_new.analysis.csv'
data = pd.read_csv(csv_file_path)

# Define the HDF5 file path
hdf5_file_path = 'tryimportSLEAP.h5'

# Write to HDF5 file
data.to_hdf(hdf5_file_path, key='data', mode='w')

print("CSV has been converted to HDF5")
