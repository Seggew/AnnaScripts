import cv2
import numpy as np
import os
from PIL import Image

frame_input_folder = '/Users/seggewa/Desktop/Visualisation/video_frames'
plot_input_folder = '/Users/seggewa/Desktop/Visualisation/frames_png'
output_folder = '/Users/seggewa/Desktop/Visualisation/overlay_frames'
os.makedirs(output_folder, exist_ok=True)

for frame_file in os.listdir(frame_input_folder):
    if frame_file.endswith('.png'):
        # Load video frame
        frame_path = os.path.join(frame_input_folder, frame_file)
        frame_image = cv2.imread(frame_path)
        
        # The frame number is embedded in the filename, extract it
        frame_number = frame_file.split('_')[1].split('.')[0]
        
        # Load the corresponding plot PNG
        plot_file = f'frame_{frame_number}.png'
        plot_path = os.path.join(plot_input_folder, plot_file)
        
        # Check if the corresponding plot PNG exists, if not, skip this frame
        if not os.path.exists(plot_path):
            print(f"No matching plot for {frame_file}, skipping.")
            continue  # Skip the frame if no matching plot
        
        plot_image = Image.open(plot_path).convert("RGBA")
        
        # Convert OpenCV frame to PIL image
        frame_pil = Image.fromarray(cv2.cvtColor(frame_image, cv2.COLOR_BGR2RGB))
        
        # Overlay the plot on the frame
        combined_image = Image.alpha_composite(frame_pil.convert("RGBA"), plot_image)
        
        # Save the resulting overlay
        combined_image = cv2.cvtColor(np.array(combined_image), cv2.COLOR_RGBA2BGR)
        output_frame_path = os.path.join(output_folder, frame_file)
        cv2.imwrite(output_frame_path, combined_image)

print(f"Overlay frames saved in {output_folder}")
