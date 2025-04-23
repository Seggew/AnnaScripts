import trackpy as tp
import pandas as pd 

data = pd.read_csv("filtered_combined_clustersSIcontrol.csv")

data['x'] = (data['x_head'] + data['x_tail']) / 2
data['y'] = (data['y_head'] + data['y_tail']) / 2

track_data = data[['frame', 'x', 'y', 'cluster', 'condition', 'clustering_path']].copy()
linked = tp.link_df(track_data, search_range=15)
result = pd.merge(data, linked[['frame', 'x', 'y', 'particle']], on=['frame', 'x', 'y'])

result.to_csv("clusters_tracked.csv", index=False)

print("Done and saved :) -> saved under clusters_tracked.csv")