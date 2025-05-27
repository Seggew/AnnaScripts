
######################

# %% PRINT UNIQUE TRACKS AND CHECK GAPS IN EACH TRACK 

import sys
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN


df = pd.read_csv('/Users/seggewa/Desktop/ConnectomeTracking/REVERSED-2025-03-27_18-46-40_SV1.tracks.000_REVERSED-2025-03-27_18-46-40_SV1.analysis.csv')

# clear the data from any erronaeously detected tracks at the bottom of the cassette (handrwriting =/= larvae)
invalid_tracks = df[df['tail.y'] > 450]['track'].unique()
df = df[~df['track'].isin(invalid_tracks)]

#adding linear interpolation to fill msising frames on my tracks

track_gaps = {}
filled_rows = []

for track_id in df['track'].unique():
    track_df = df[df['track'] == track_id].sort_values(by='frame_idx')
    frames = track_df['frame_idx'].tolist()
    min_frame, max_frame = min(frames), max(frames)

    missing_frames = [f for f in range(min_frame, max_frame + 1) if f not in frames]
    
    keypoint_fields = ['head.x', 'head.y', 'tail.x', 'tail.y']  # Add more as needed

if missing_frames:
    track_gaps[track_id] = missing_frames

    for missing_frame in missing_frames:
        # Find previous and next frames
        prev_df = track_df[track_df['frame_idx'] < missing_frame]
        next_df = track_df[track_df['frame_idx'] > missing_frame]

        if prev_df.empty or next_df.empty:
            continue  # Can't interpolate without both sides

        prev_frame = prev_df.iloc[-1]
        next_frame = next_df.iloc[0]

        total_steps = next_frame['frame_idx'] - prev_frame['frame_idx']
        step = missing_frame - prev_frame['frame_idx']
        weight = step / total_steps

        # Interpolate each keypoint field
        filled_row = {
            'track': track_id,
            'frame_idx': missing_frame
        }

        for key in keypoint_fields:
            prev_val = prev_frame.get(key)
            next_val = next_frame.get(key)

            if pd.notnull(prev_val) and pd.notnull(next_val):
                interp_val = prev_val + weight * (next_val - prev_val)
            else:
                interp_val = np.nan  # fallback if one side is missing

            filled_row[key] = interp_val

        # Optionally interpolate additional fields like scores
        # Example:
        # for score_key in ['head.score', 'tail.score']:
        #     prev_score = prev_frame.get(score_key)
        #     next_score = next_frame.get(score_key)
        #     if pd.notnull(prev_score) and pd.notnull(next_score):
        #         filled_row[score_key] = prev_score + weight * (next_score - prev_score)

        filled_rows.append(filled_row)


# Add interpolated rows and sort the data frame
if filled_rows:
    df = pd.concat([df, pd.DataFrame(filled_rows)], ignore_index=True)

df = df.sort_values(by=['track', 'frame_idx']).reset_index(drop=True)

#DBSCAN
# Calculate vectors for each instance (tail - head)
df['vector_x'] = df['tail.x'] - df['head.x']
df['vector_y'] = df['tail.y'] - df['head.y']

# Define the custom distance function
def custom_distance(A, B):
    tail_A = A[:2]  # x_tail and y_tail of A
    tail_B = B[:2]  # x_tail and y_tail of B
    euclidean_tail_dist = np.linalg.norm(tail_A - tail_B)

    vector_A = A[2:]
    vector_B = B[2:]
    magnitude_A = np.linalg.norm(vector_A)
    magnitude_B = np.linalg.norm(vector_B)

    if magnitude_A == 0 or magnitude_B == 0:
        return 1000

    cos_similarity = np.dot(vector_A, vector_B) / (magnitude_A * magnitude_B)

    if cos_similarity > 0.7:  # <-- you can adjust this threshold as needed
        return euclidean_tail_dist

    return 1000

# Run DBSCAN per frame
clustering_results = []
for frame, group in df.groupby('frame_idx'):  # <-- assuming renaming happens later
    # Drop rows with any NaNs in relevant columns
    group = group.dropna(subset=['tail.x', 'tail.y', 'vector_x', 'vector_y'])
    
    if len(group) < 3:
        group['cluster'] = -1
        clustering_results.append(group)
        continue

    data_for_clustering = group[['tail.x', 'tail.y', 'vector_x', 'vector_y']].values

    dbscan = DBSCAN(eps=45, min_samples=3, metric=custom_distance)
    labels = dbscan.fit_predict(data_for_clustering)

    group = group.copy()
    group['cluster'] = labels
    clustering_results.append(group)


# Merge results back into a single dataframe
df = pd.concat(clustering_results, ignore_index=True)

######################
# %% CHECK FRAMES IN WHICH ALL ANIMALS WERE NOT PREDICTED

# frames with a mix of NaN and values in instance.score indicate missing predictions on those frames

# frames_with_mixed_scores = df.groupby('frame_idx')['instance.score'].apply(
#     lambda x: x.isna().any() and x.notna().any()
# )

# mixed_frames = frames_with_mixed_scores[frames_with_mixed_scores].index

# print(f"Frames:{mixed_frames}")


######################
# %% RENAME COLUMNS 




df.rename(columns={'frame_idx': 'frame', 'track': 'track_id', 'head.x': 'x_head', 'head.y': 'y_head', 'body.x': 'x_body', 'body.y': 'y_body', 'tail.x': 'x_tail', 'tail.y': 'y_tail', 'instance.score': 'instance_score', 'head.score': 'score_head', 'body.score': 'score_body', 'tail.score': 'score_tail'}, inplace=True)

df['track_id'] = df['track_id'].str.replace('track_', '', regex=True).astype(int)


#df = df.drop(columns=['displacement'])

df.to_feather('/Users/seggewa/Desktop/ConnectomeTracking/REVERSED-2025-03-27_18-46-40_SV1.tracks.feather')
#print(df.columns)

print("done")


# %% CSV -> FEATHER AND SLP

#df.to_feather('/Volumes/lab-windingm/home/users/cochral/AttractionRig/Videos/socially-isolated/N10/FOOD/feather.feather')








#############################################################
