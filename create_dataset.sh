#!/bin/bash

SOURCE="images"
DEST="train_images"
TARGET=2000

if [ -f "venv/bin/python3" ]; then
    PYTHON="venv/bin/python3"
elif [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
else
    PYTHON=$(which python3)
fi

echo "Using Python: $PYTHON"

mkdir -p "$DEST"

find "$SOURCE" -maxdepth 1 -mindepth 1 -type d | while read -r dir; do
    cat_name=$(basename "$dir")
    mkdir -p "$DEST/$cat_name"

    count=$(find "$dir" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | wc -l)

    echo "--- Category: $cat_name ($count images) ---"

    if [ "$count" -ge "$TARGET" ]; then
        echo "Too many or enough images. Copying first $TARGET..."
        find "$dir" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | head -n "$TARGET" | xargs -I {} cp {} "$DEST/$cat_name/"
    else
        echo "Not enough images. Copying all ($count) and augmenting..."
        cp "$dir"/* "$DEST/$cat_name/" 2>/dev/null

        needed=$((TARGET - count))
        runs=$(( (needed + 5) / 6 ))

        mapfile -t to_augment < <(find "$DEST/$cat_name" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \))
        num_to_augment=${#to_augment[@]}

        if [ "$num_to_augment" -gt 0 ]; then
            echo "Starting $runs augmentations..."
            for ((i=0; i<runs; i++)); do
                idx=$((i % num_to_augment))
                target_file="${to_augment[$idx]}"

                "$PYTHON" Augmentation.py "$target_file" &

                if (( $(jobs -r | wc -l) >= $(nproc) )); then
                    wait -n
                fi
            done
            wait
        fi
    fi
done

echo "--- Done! Check the '$DEST' folder. ---"