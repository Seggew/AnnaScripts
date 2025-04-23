import pandas as pd

data = pd.read_csv("combined_clustersDBSCAN.csv")


data_filtered = data[(data['frame'] >= 25000) & (data['frame'] <= 150000)]

data_toy = data_filtered[data_filtered['frame'] % 100 == 0]

data_toy.to_csv("filtered_combined_clustersSIcontrol.csv", index=False)
