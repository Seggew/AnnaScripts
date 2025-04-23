#!/bin/bash
#SBATCH --job-name=convert_h264_to_mp4  # Job name
#SBATCH --output=convert_h264_to_mp4.log  # Output log file
#SBATCH --error=convert_h264_to_mp4.err   # Error log file
#SBATCH --time=06:00:00  # Time limit
#SBATCH --ntasks=1       # Number of tasks (processes)
#SBATCH --cpus-per-task=4  # Number of CPU cores per task
#SBATCH --mem=4G         # Memory per node
#SBATCH --partition=ncpu  # Partition (queue)

# Load the required module (adjust based on your HPC system)
module load ffmpeg

# Change to the directory where the .h264 files are located
cd /camp/home/seggewa/home/shared/SVvidsShare/9_12_24_SVvidsAnnaLucy

# Convert .h264 files to .mp4
for f in *.h264; do
    ffmpeg -i "$f" -c:v libx264 -profile:v baseline -level 3.0 -c:a aac -strict experimental "${f%.h264}.mp4"
done
