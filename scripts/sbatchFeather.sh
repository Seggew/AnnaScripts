#!/bin/bash
#SBATCH --job-name=cluster_analysis     # Job name
#SBATCH --output=cluster_analysis_%j.out # Output file
#SBATCH --error=cluster_analysis_%j.err  # Error file
#SBATCH --time=15:00:00                 # Time limit (HH:MM:SS)
#SBATCH --mem=40G                        # Memory required
#SBATCH --cpus-per-task=16               # Number of CPU cores
#SBATCH --partition=ncpu
#SBATCH --mail-user=$(whoami)@crick.ac.uk
#SBATCH --mail-type=FAIL


ml purge
ml Anaconda3/2023.09-0
source /camp/apps/eb/software/Anaconda/conda.env.sh

conda activate analysis

python FeatherAnalysisSLEAP.py
