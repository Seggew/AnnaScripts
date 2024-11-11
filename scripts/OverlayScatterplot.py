import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import os

# Step 1: Load the CSV file
file_path = '/Users/seggewa/Desktop/gridsearch/SORTTESTbest_performance.csv'  # Update with your actual file path
image_path = '/Users/seggewa/Desktop/gridsearch/1FRAME2024-08-29_14-01-33_SV2.png'
data = pd.read_csv(file_path) 

# Load the PNG image directly
frame = cv2.imread(image_path)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB for correct color display in matplotlib

# Select the data for the frame
frame_data = data[data['frame'] == data['frame'].iloc[0]]  # Assuming you want the first frame data

# Plot the image and overlay data
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(frame)
sns.scatterplot(x=frame_data['x_tail'], y=frame_data['y_tail'], hue=frame_data['cluster'], ax=ax, s=40, palette='viridis')
ax.set_aspect('equal', adjustable='box')
plt.legend(title='Cluster')
plt.show()

# Save the plot
# plt.savefig('/Users/seggewa/Desktop/gridsearch/!!!SV2-GS-PARAMETERSTEST.png', bbox_inches='tight', dpi=300)
