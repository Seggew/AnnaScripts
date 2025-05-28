import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



data = pd.read_feather('/Users/seggewa/Desktop/ConnectomeTracking/2025-01-07_14-46-15_SV18.tracks.feather')

data = data[data['frame'] >= 25000]
clustered_data = data[data['cluster'] != -1]
tracked_data = clustered_data[clustered_data['track_id'] <= 18]

frames_in_cluster = tracked_data.groupby('track_id')['frame'].nunique().reset_index()
frames_in_cluster.columns = ['track_id', 'frames_in_cluster']

frames_in_cluster = frames_in_cluster.sort_values(by='frames_in_cluster', ascending=False)

# Plotting
plt.figure(figsize=(14, 6))
sns.barplot(data=frames_in_cluster, x='track_id', y='frames_in_cluster', palette='viridis')
plt.xticks(rotation=90)
plt.xlabel('Track ID')
plt.ylabel('Number of Frames in a Cluster')
plt.title('Number of Clustered Frames per Track')
plt.tight_layout()
plt.show()