#%%import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import numpy as np
import os

# Step 1: Load the CSV file
file_path = '/Users/seggewa/Desktop/cluster/DBSCAN1-10-eps60.csv'  # Update with your actual file path
video_path = '/Users/seggewa/Desktop/cluster/1hrTRIM2024-08-29_14-01-33_SV2.mp4'
data = pd.read_csv(file_path) 

#%% video into numpy
# Ensure frame numbers are integers
# Ensure frame numbers are integers
frames_to_extract = data['frame'].unique().astype(int)[:1]

# Proceed with frame extraction as before
video = cv2.VideoCapture(video_path)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
extracted_frames = {}

for frame_number in frames_to_extract:
    if frame_number < total_frames:
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        success, frame = video.read()
        if success:
            extracted_frames[frame_number] = frame
        else:
            print(f"Error: Could not read frame {frame_number}.")
    else:
        print(f"Frame {frame_number} exceeds total number of frames in video.")
video.release()

# Access frame using the integer key
frame = extracted_frames[frames_to_extract[0]]

fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(frame)
frame_data = data[data['frame'] == frames_to_extract[0]]

# Plot with color based on cluster column
sns.scatterplot(x=frame_data['x_tail'], y=frame_data['y_tail'], hue=frame_data['cluster'], ax=ax, s=40, palette='viridis')
ax.set_aspect('equal', adjustable='box')
plt.legend(title='Cluster')
#plt.show()
plt.savefig('plots/28-10-24-DBSCAN1-10-eps60.png', bbox_inches='tight', dpi=300)

