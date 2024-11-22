import cv2
import os

def extract_frame(video_path, frame_number):
    # Ensure frame_number is a single integer
    if isinstance(frame_number, tuple):
        print("Error: frame_number was provided as a tuple. Please provide a single integer.")
        return
    frame_number = int(frame_number)  # Convert to integer if it's valid

    # Load the video
    cap = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    # Get the total number of frames to check if frame_number is in range
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_number < 0 or frame_number >= total_frames:
        print(f"Error: Frame number {frame_number} is out of range. Video has {total_frames} frames.")
        cap.release()
        return

    # Set the frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read the frame
    success, frame = cap.read()
    if not success:
        print(f"Error: Could not read frame {frame_number}")
        cap.release()
        return
    
    # Create the output file path with .png extension
    base_name = os.path.splitext(video_path)[0]
    output_path = f"{base_name}_frame{frame_number}.png"
    
    # Save the frame as a PNG
    cv2.imwrite(output_path, frame)
    print(f"Frame {frame_number} saved as {output_path}")
    
    # Release the video capture object
    cap.release()


# Usage
video_path = "/Users/seggewa/Desktop/ExtractFrames/2024-08-23_11-23-53_SV15.mp4"  # Replace with your video file path
frame_number = 126520  # Replace with the specific frame number you want to extract
extract_frame(video_path, frame_number)
