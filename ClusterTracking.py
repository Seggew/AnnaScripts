import trackpy as tp
import pandas as pd 

data = pd.read_csv("filtered_combined_clustersSIcontrol.csv")
#data_filtered = dataOrigin[(dataOrigin['frame'] >= 25000) & (data['frame'] <= 150000)]

data = data[data['cluster'] >= 0]

centroids = (
    data.groupby(['origin_file', 'frame', 'cluster'])
    .agg({
        'x_head': 'mean',
        'y_head': 'mean',
        'x_tail': 'mean',
        'y_tail': 'mean',
        'condition': 'first',           # keep metadata (e.g. condition)
        'clustering_path': 'first'       # and clustering path
    })
    .reset_index()
)

centroids['x'] = (centroids['x_head'] + centroids['x_tail']) / 2
centroids['y'] = (centroids['y_head'] + centroids['y_tail']) / 2


track_data = centroids[['origin_file', 'frame', 'x', 'y', 'cluster', 'condition', 'clustering_path']].copy()

all_tracked = []
for origin, group in track_data.groupby('origin_file'):
    linked = tp.link_df(group, search_range=100)
    linked['origin_file'] = origin  # Add back origin_file info
    all_tracked.append(linked)

linked = tp.link_df(track_data, search_range=15)
tracked_df = pd.concat(all_tracked, ignore_index=True)

tracked_df.to_csv("clusters_tracked.csv", index=False)

print("Done and saved :) -> saved under clusters_tracked.csv")