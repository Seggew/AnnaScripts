# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from natsort import natsorted

# Load the master CSV file
master_csv_path = '/Users/seggewa/Desktop/Combined_clustersDBSCAN.csv'
data = pd.read_csv(master_csv_path)

# natural sorting (prevent 100, 150, 50 situations)
data_sorted = data.loc[natsorted(data.index, key=lambda x: data['condition'][x])] 

# %%
# plotting the plot
fig, ax = plt.subplots(1,1, figsize=(5,4))
sns.barplot(x=data_sorted.condition, y=data_sorted.cluster, errorbar='sd', color='#B8CCC3', ax=ax)
plt.xticks(rotation=45, ha='right')

# saving the plot, make sure it is in the same cell
plt.savefig('plots/ClusterDennis.png', bbox_inches='tight', dpi=300)

# %%
