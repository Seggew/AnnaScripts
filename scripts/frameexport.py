import cv2
import os
import pandas as pd

# Load the CSV file to get the specific frames you need
csv_path = '/Users/seggewa/Desktop/cluster/30x3-ClusterAnalysis_1hrTRIM2024-08-29_14-01-33_SV2.tracks.csv'  # Update this path to your CSV file
data = pd.read_csv(csv_path)

# Get the unique frame numbers from the CSV
frames_needed = data['Frame'].unique()

video_path = '/Users/seggewa/Desktop/cluster/1hrTRIM2024-08-29_14-01-33_SV2.mp4'
frame_output_folder = '/Users/seggewa/Desktop/cluster/video_frames'
os.makedirs(frame_output_folder, exist_ok=True)

# Capture the video
video = cv2.VideoCapture(video_path)
total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Make sure to track which frames we need to save
frame_count = 0
success = True

# Loop through the video and only extract the frames specified in the CSV
while success:
    success, image = video.read()
    
    if frame_count in frames_needed:
        # Save the frame with the exact frame number from the video
        frame_path = os.path.join(frame_output_folder, f'frame_{frame_count}.png')
        cv2.imwrite(frame_path, image)
    
    frame_count += 1
    
    # Break the loop when we reach the total number of frames
    if frame_count > total_frames:
        break

video.release()
print(f"Frames extracted and saved to {frame_output_folder}")
