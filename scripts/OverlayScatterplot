#%%import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import numpy as np
import os

# Step 1: Load the CSV file
file_path = '/Users/seggewa/Desktop/cluster/30x3-ClusterAnalysis_1hrTRIM2024-08-29_14-01-33_SV2.tracks.csv'  # Update with your actual file path
video_path = '/Users/seggewa/Desktop/cluster/1hrTRIM2024-08-29_14-01-33_SV2.mp4'
data = pd.read_csv(file_path) 

#%% video into numpy
frames_to_extract = data['Frame'].unique()
video = cv2.VideoCapture(video_path)

total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
extracted_frames = {}
for frame_number in frames_to_extract:
    if frame_number < total_frames:
        # Set the video to the specific frame
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        # Read the frame
        success, frame = video.read()

        if success:
            # Convert the frame (which is already a NumPy array)
            extracted_frames[frame_number] = frame
            print(f"Frame {frame_number} extracted as NumPy array.")
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.imshow(frame)
            frame_data = data[data['Frame'] == frame_number]
            sns.scatterplot(x=frame_data['x_tail'], y=frame_data['y_tail'], ax=ax, s=40)
            ax.set_aspect('equal', adjustable='box')
            plt.show()

        else:
            print(f"Error: Could not read frame {frame_number}.")
    else:
        print(f"Frame {frame_number} exceeds total number of frames in video.")

# Release the video object
video.release()
