#!/bin/bash
#SBATCH --job-name=cluster_analysis     # Job name
#SBATCH --output=cluster_analysis_%j.out # Output file
#SBATCH --error=cluster_analysis_%j.err  # Error file
#SBATCH --time=01:00:00                 # Time limit (HH:MM:SS)
#SBATCH --mem=4G                        # Memory required
#SBATCH --cpus-per-task=2               # Number of CPU cores

# Load necessary modules (if any)
module load python/3.x  # Ensure the appropriate Python module is loaded (adjust as needed)

# Run the Python script from the directory where the sbatch script is located
python cluster_analysis.py
