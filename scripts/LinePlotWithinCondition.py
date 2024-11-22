import pandas as pd
import matplotlib.pyplot as plt

# Load the data
data_file_path = '/Users/seggewa/Desktop/Combined_clustersDBSCAN.csv'  # Replace with the actual file path
df = pd.read_csv(data_file_path)

# Filter data for the selected condition (e.g., '150eggs')
df = df[df['condition'] == '100eggs']

# Step 1: Identify experiment boundaries
# Mark the start of each experiment using `frame=0` and `track_id=0`
df['experiment_id'] = ((df['frame'] == 0) & (df['track_id'] == 0)).cumsum()

# Filter out frames beyond 400000 within each experiment
df = df[df['frame'] <= 400000]

# Step 2: Calculate fraction of track_id's in clusters (cluster > -1) per frame for each experiment
df['in_cluster'] = (df['cluster'] > -1).astype(int)
fractions = df.groupby(['experiment_id', 'frame'])['in_cluster'].mean().reset_index()

# Step 3: Plot individual graphs for each experiment
plt.figure(figsize=(12, 8))

for experiment_id, group in fractions.groupby('experiment_id'):
    plt.plot(
        group['frame'], 
        group['in_cluster'], 
        label=f'Experiment {experiment_id}', 
        linewidth=2
    )

# Add labels, title, and legend
plt.xlabel('Frame (Time)', fontsize=14)
plt.ylabel('Fraction of Track IDs in Clusters', fontsize=14)
plt.title('Clustering for Condition 150eggs (Individual Experiments)', fontsize=16)
plt.legend(title='Experiments', fontsize=8)
plt.grid(True, linestyle='--', alpha=0.5)

# Show the plot
plt.show()
