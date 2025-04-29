import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
#2025-03-03_22-15-15_SV13
data = pd.read_csv('clusters_tracked.csv')
output_folder = '/Users/seggewa/Desktop/Tracking.png'
file='2025-03-03_22-15-15_SV13.predictions_DBSCAN-eps-43_cos-0.86.feather'
Keydata = data[data['origin_file'] == file]
for frame in Keydata['frame'].unique():
    frame_data = Keydata[Keydata['frame'] == frame]
    plt.figure(figsize=(9, 5.5))
    sns.scatterplot(
        data=frame_data,
        x='x',
        y='y',
        hue='cluster',
        s=60
    )
    plt.xlim(0, 1800)
    plt.ylim(1100, 0)
    plt.title(f"Frame {frame} - Clusters")
    plt.xlabel('x pixel')
    plt.ylabel('y pixel')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/frame_{frame:03d}.png", bbox_inches='tight', pad_inches=0)
    plt.close()

print("saved under /Users/seggewa/Desktop/Tracking.png ")