#%%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import os
import numpy as np 
from PIL import Image

#%%
#2025-03-03_22-15-15_SV13
Keydata = pd.read_csv('clusters_tracked.csv')
video_path = 'data/2024-12-10_16-37-52_SV23.mp4'
scatterfolder = '/Users/seggewa/Desktop/QuickSaveClusterScatter'
output_folder = '/Users/seggewa/Desktop/OverlayTrackedClustersOnTracks'
os.makedirs(output_folder, exist_ok=True)
os.makedirs(scatterfolder, exist_ok=True)

#%%
#file='/data/2024-12-10_16-37-52_SV23.predictions_DBSCAN-eps-43_cos-0.86.feather'
#Keydata = data[data['origin_file'] == file]

video = cv2.VideoCapture(video_path)
fps = video.get(cv2.CAP_PROP_FPS)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

for frame in Keydata['frame'].unique():
    
    video.set(cv2.CAP_PROP_POS_FRAMES, frame)
    ret, frame_image = video.read()
    frame_data = Keydata[Keydata['frame'] == frame]
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=100)
    sns.scatterplot(
        data=frame_data,
        x='x',
        y='y',
        hue='cluster',
        s=60,
        ax=ax

        # Plot head position
    # plt.scatter(
    #     frame_data['x_head'],
    #     frame_data['y_head'],
    #     color='red',
    #     s=30,
    #     marker='^',
    #     label='head'
    # )

    # Plot tail position
    # plt.scatter(
    #     frame_data['x_tail'],
    #     frame_data['y_tail'],
    #     color='blue',
    #     s=30,
    #     marker='v',
    #     label='tail'
    # )
    )
    ax.set_xlim(0,1800)
    ax.set_ylim(1100, 0)
    ax.axis('off')

    #plt.xlim(0, 1800)
    #plt.ylim(1100, 0)
    #plt.title(f"Frame {frame} - Clusters")
    #plt.xlabel('x pixel')
    #plt.ylabel('y pixel')
    plt.tight_layout()
    plt.savefig(f"{output_folder}/frameOVERLAY_{frame:03d}.png", bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

    if not os.path.exists(scatter_overlay_path):
        print(f"Warning: Failed to save scatterplot overlay for frame {frame}")
        continue  # Skip this frame

    #combine scatterplot with video frames
    scatter_overlay_path = f"{output_folder}/frameOVERLAY_{frame:03d}.png"
    scatter_img = Image.open(scatter_overlay_path).convert("RGBA")  

    frame_pil = Image.fromarray(cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB)).convert("RGBA")
    combined = Image.alpha_composite(frame_pil, scatter_img)

    combined_bgr = cv2.cvtColor(np.array(combined), cv2.COLOR_RGBA2BGR)
    cv2.imwrite(f"{output_folder}/frame_{frame:04d}.png", combined_bgr)

print("saved under /Users/seggewa/Desktop/OverlayTrackedClustersOnTracks ")
# %%
