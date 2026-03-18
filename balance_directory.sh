#!/bin/bash

# Check arguments
if [ $# -ne 2 ]; then
  echo "Usage: $0 <number_of_images_to_process> <directory>"
  exit 1
fi

total_images=$1
dir=$2

# Validate number
if ! [[ "$total_images" =~ ^[0-9]+$ ]]; then
  echo "Error: first argument must be a number"
  exit 1
fi

# Validate directory
if [ ! -d "$dir" ]; then
  echo "Error: '$dir' is not an existing directory"
  exit 1
fi

# Count actual files in the directory
existing_files=$(ls "$dir"/image\ \(*.JPG 2>/dev/null | wc -l)

if [ "$existing_files" -eq 0 ]; then
  echo "No files found in $dir"
  exit 1
fi

# Compute how many executions are needed
count=$(( (total_images + 5) / 6 ))  # ceil division by 6

# Limit count to available files
if [ "$count" -gt "$existing_files" ]; then
  count=$existing_files
fi

# Safe parallelism
MAX_JOBS=$(nproc)

for ((i=1; i<=count; i++)); do
  file="$dir/image ($i).JPG"

  if [ -f "$file" ]; then
    venv/bin/python3.13 Augmentation.py "$file" &
  else
    echo "File not found: $file. Stopping loop."
  fi

  # Limit concurrent jobs
  if (( $(jobs -r | wc -l) >= MAX_JOBS )); then
    wait -n
  fi
done

wait
echo "Augmentation completed."