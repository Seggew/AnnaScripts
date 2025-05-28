#!/bin/bash

# Usage: ./safe_move.sh /path/to/source /path/to/destination
# before running this file for the first time, run "chmod +x safe_move.sh" to make it executable

SOURCE="$1"
DEST="$2"
LOGFILE="$DEST/safe_move_$(date +%Y%m%d_%H%M%S).log"

# Check if both source and destination are provided
if [[ -z "$SOURCE" || -z "$DEST" ]]; then
  echo "Usage: $0 /path/to/source /path/to/destination" | tee -a "$LOGFILE"
  exit 1
fi

# Check if source directory exists
if [[ ! -d "$SOURCE" ]]; then
  echo "Error: Source directory does not exist: $SOURCE" | tee -a "$LOGFILE"
  exit 2
fi

mkdir -p "$DEST"

echo "Starting safe move from $SOURCE to $DEST" | tee -a "$LOGFILE"

# Step 1: Copy using rsync
echo "Copying files..." | tee -a "$LOGFILE"
rsync -av --progress "$SOURCE/" "$DEST/" >> "$LOGFILE" 2>&1

if [[ $? -ne 0 ]]; then
  echo "Error during rsync copy. Check $LOGFILE for details." | tee -a "$LOGFILE"
  exit 3
fi

# Step 2: Verify using rsync dry run with checksum
echo "Verifying file integrity..." | tee -a "$LOGFILE"
rsync -rcn "$SOURCE/" "$DEST/" > /tmp/rsync_verify.tmp 2>>"$LOGFILE"

if grep -q -v '/$' /tmp/rsync_verify.tmp; then
  echo "Verification failed! Differences found between source and destination:" | tee -a "$LOGFILE"
  cat /tmp/rsync_verify.tmp | tee -a "$LOGFILE"
  rm /tmp/rsync_verify.tmp
  exit 4
else
  echo "Verification successful. No differences found." | tee -a "$LOGFILE"
  rm /tmp/rsync_verify.tmp
fi

# Step 3: Delete source files and directories
echo "Deleting original source directory..." | tee -a "$LOGFILE"
rm -r "$SOURCE"

if [[ $? -ne 0 ]]; then
  echo "Error deleting source directory: $SOURCE" | tee -a "$LOGFILE"
  exit 5
fi

echo "Safe move completed successfully." | tee -a "$LOGFILE"
exit 0
