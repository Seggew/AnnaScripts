import os
import re
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import adjusted_rand_score
from sklearn.model_selection import ParameterGrid
from scipy.stats import mode  # Import mode from scipy

# Directory containing the CSV, Feather, and PNG files
data_dir = "/Users/seggewa/Desktop/ExtractFrames"

# Regex pattern to extract the identifier and frame number from filenames
pattern = re.compile(r"(\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}_SV\d)")
frame_pattern = re.compile(r"_frame(\d+)\.png")

# Collect ground truth and feather files and their identifiers
ground_truth_files = {}
feather_files = {}
frame_numbers = {}

# Scan through files in the directory
for file_name in os.listdir(data_dir):
    file_path = os.path.join(data_dir, file_name)
    
    # Identify ground truth CSV files
    if file_name.startswith("GT") and file_name.endswith(".csv"):
        identifier = pattern.search(file_name).group(1)
        ground_truth_files[identifier] = file_path
    
    # Identify Feather files
    elif file_name.endswith(".feather"):
        identifier = pattern.search(file_name).group(1)
        feather_files[identifier] = file_path
    
    # Extract frame numbers from PNG filenames
    elif file_name.endswith(".png") and "_frame" in file_name:
        identifier = pattern.search(file_name).group(1)
        frame_number = int(frame_pattern.search(file_name).group(1))
        frame_numbers[identifier] = frame_number

# Verify that ground truth, feather, and frame number match for each identifier
valid_identifiers = set(ground_truth_files.keys()) & set(feather_files.keys()) & set(frame_numbers.keys())

# Define parameter grid for eps and cosine similarity threshold
param_grid = {
    'eps': np.round(np.linspace(10, 100, 50), 2),  # 50 values for eps between 10 and 100, rounded to 2 decimals
    'cosine_threshold': np.round(np.linspace(0, 1, 50), 2)  # 50 values for cosine_threshold between 0 and 1, rounded to 2 decimals
}

# Initialize a list to store ARI scores and parameter results
grid_search_results = []

# Define custom distance function with eps and cosine similarity threshold
def custom_distance(A, B, eps, cosine_threshold):
    tail_A = A[:2]
    tail_B = B[:2]
    euclidean_tail_dist = np.linalg.norm(tail_A - tail_B)
    
    vector_A = A[2:]
    vector_B = B[2:]
    magnitude_A = np.linalg.norm(vector_A)
    magnitude_B = np.linalg.norm(vector_B)
    
    if magnitude_A == 0 or magnitude_B == 0:
        return 1000  # Treat zero-magnitude vectors as far apart
    
    cos_similarity = np.dot(vector_A, vector_B) / (magnitude_A * magnitude_B)
    
    if euclidean_tail_dist <= eps and cos_similarity > cosine_threshold:
        return euclidean_tail_dist
    return 1000  # Large distance if either condition fails

# Loop through each parameter combination
for params in ParameterGrid(param_grid):
    ari_scores = []  # Store ARI scores for each ground truth-data pair for the current parameter set
    
    # Loop through each valid identifier (matched CSV, Feather, and frame number)
    for identifier in valid_identifiers:
        gt_path = ground_truth_files[identifier]
        feather_path = feather_files[identifier]
        frame_number = frame_numbers[identifier]

        # Load data and ground truth
        data = pd.read_feather(feather_path)
        ground_truth = pd.read_csv(gt_path)

        # Ensure both data and ground truth have the necessary columns
        data['frame'] = data['frame'].astype(int)
        ground_truth['frame'] = ground_truth['frame'].astype(int)

        # Filter data for the specified frame only and drop rows with missing values
        filtered_data = data[data['frame'] == frame_number].dropna(subset=['x_head', 'y_head', 'x_tail', 'y_tail'])
        ground_truth_frame = ground_truth[ground_truth['frame'] == frame_number]

        # Sort both datasets by the x_tail coordinate for alignment
        filtered_data = filtered_data.sort_values(by='x_tail').reset_index(drop=True)
        ground_truth_frame = ground_truth_frame.sort_values(by='x_tail').reset_index(drop=True)

        # Calculate vectors (tail - head) for each instance in filtered_data
        filtered_data['vector_x'] = filtered_data['x_tail'] - filtered_data['x_head']
        filtered_data['vector_y'] = filtered_data['y_tail'] - filtered_data['y_head']

        # Get vectors and ground truth clusters
        vectors = filtered_data[['x_tail', 'y_tail', 'vector_x', 'vector_y']].values
        gt_clusters = ground_truth_frame['cluster'].values

        # Apply DBSCAN with the current parameter set
        dbscan = DBSCAN(eps=params['eps'], min_samples=3, metric=lambda A, B: custom_distance(A, B, params['eps'], params['cosine_threshold']))
        labels = dbscan.fit_predict(vectors)
        
        # Calculate ARI for the current file pair and parameter set
        ari_score = adjusted_rand_score(gt_clusters, labels)
        ari_scores.append(ari_score)

    # Calculate the mean, median, and mode ARI scores for the current parameter set
    avg_ari_score = np.mean(ari_scores)
    median_ari_score = np.median(ari_scores)
    mode_ari_score = mode(ari_scores).mode[0] if ari_scores else np.nan  # Mode can be NaN if ari_scores is empty

    # Append the results to the grid search results
    grid_search_results.append({
        'eps': params['eps'],
        'cosine_threshold': params['cosine_threshold'],
        'average_ari_score': avg_ari_score,
        'median_ari_score': median_ari_score,
        'mode_ari_score': mode_ari_score
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(grid_search_results)

# Save the grid search results to a CSV for analysis
results_df.to_csv('/Users/seggewa/Desktop/done/50x50ARI_16statistics.csv', index=False)
print("Grid search results saved.")
