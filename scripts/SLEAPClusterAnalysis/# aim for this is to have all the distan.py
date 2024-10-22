# aim for this is to have all the distances between every pair of larvae in a video. From these pairs, I want to take a threshold of the distance between each pair and if it is below a certain value, this pair counts as clustering.
# one cluster has to be ≥3 animals. The %of animals engaged in a cluster across all frames will then be compared across videos and conditions

import os
import pandas as pd
import numpy as np
import seaborn as sns
import %matplotlib inline
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# tracking data is not great yet so will focus on tail node, as this is what is close in digging clusters
# Step 1: want a dictionary which holds the average distance between every combination of tracks per unique frame

df = pd.read_csv('/Users/seggewa/Desktop/DataAnalysis/2024-02-05_all-labels_tracks.v007.000_2023_11_13_white_ON_1800,1100_totalpixels-1980000_new.analysis.csv')


average_distance_dict = {}  # empty dictionary


for frame in df['frame_idx'].unique():
    
    unique_frame = df[df['frame_idx'] == frame] # filter to ensure the frame is unique 
    
    # cdist function requires two 2-dimensional array-like objects as inputs
    # create an array of the coordinates for that specific frame

    body_coordinates = unique_frame[['spiracle.x', 'spiracle.y']].to_numpy()

    # The cdist function computes the distance between every pair of points in the two arrays passed to it.

    distance = cdist(body_coordinates, body_coordinates, 'euclidean')

    # the cdist function will also calculate the distance between the same tracks e.g. track 1 to track 1 
    # there will be 0s which should be exluded 
    # dont want to just ignore the 0s incase an animal is on top of one another 
    # the cdist function calculates the distances between tracks in a matrix fashion 
    # so can ignore the diagonal values which would refer distance between identical tracks 

    np.fill_diagonal(distance, np.nan)

    average_distance = np.nanmean(distance)

    pixel_to_cm =  6.3/1500 # conversion factor 

    average_distance = average_distance * pixel_to_cm 

    # store average distance value in dictionary with the frame as the key  

    average_distance_dict[frame] = average_distance  



# Creating a DataFrame
df_average_distances = pd.DataFrame({
    'frame_idx': average_distance_dict.keys(),
    'average_distance': average_distance_dict.values()})

df_average_distances

