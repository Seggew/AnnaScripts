import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example DataFrame for illustration (replace with actual CSV file)
data_file_path = '/Users/seggewa/Desktop/Combined_clustersDBSCAN.csv'  # Replace with the actual file path
df = pd.read_csv(data_file_path)

# Step 1: Create a `group_id` to separate consecutive `frame=0`s
df['group_id'] = (df['frame'] != df['frame'].shift()).cumsum()

# Step 2: Filter data for frames that are multiples of 10
filtered_data = df[(df['frame'] % 10 == 0)]

# Step 3: Calculate fractions
def calculate_fraction(group):
    # Group by `frame` within the same group_id
    frame_fractions = group.groupby(['group_id', 'frame']).apply(
        lambda x: x['in_cluster'].sum() / len(x)
    ).reset_index(name='fraction')
    return frame_fractions

# Add a binary column to indicate if a track_id is in a cluster
filtered_data['in_cluster'] = (filtered_data['cluster'] > -1).astype(int)

# Compute fractions
fractions = calculate_fraction(filtered_data)

# Step 4: Convert frames to time (hours)
filtered_data['time_in_hours'] = filtered_data['frame'] / (5 * 3600)  # Convert to hours

# Filter for first 5 hours
filtered_data = filtered_data[filtered_data['time_in_hours'] <= 5]

# Step 5: Plot the results
plt.figure(figsize=(12, 8))
sns.lineplot(data=fractions, x='frame', y='fraction', hue='group_id')

# Customize x-axis for hours
plt.xticks(range(0, 301, 60))  # Adjust tick range and intervals if needed
plt.xlabel('Time (Hours)', fontsize=14)
plt.ylabel('Fraction of Track IDs in Clusters', fontsize=14)
plt.title('Fraction of Track IDs in Clusters by Frame', fontsize=16)
plt.legend(title='Group ID', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()
