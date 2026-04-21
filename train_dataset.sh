#!/bin/bash

SOURCE="images"
DEST="train_images"
TARGET=2000

# --- DETECTION DU PYTHON ---
# On cherche d'abord si un venv est activé, sinon on cherche python3
if [ -f "venv/bin/python3" ]; then
    PYTHON="venv/bin/python3"
elif [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
else
    PYTHON=$(which python3)
fi

echo "Using Python: $PYTHON"

# 1. Création du dossier de destination
mkdir -p "$DEST"

# Utilisation d'une boucle qui gère les espaces
find "$SOURCE" -maxdepth 1 -mindepth 1 -type d | while read -r dir; do
    cat_name=$(basename "$dir")
    mkdir -p "$DEST/$cat_name"

    # Compter proprement les fichiers
    count=$(find "$dir" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | wc -l)

    echo "--- Category: $cat_name ($count images) ---"

    if [ "$count" -ge "$TARGET" ]; then
        echo "Too many or enough images. Copying first $TARGET..."
        find "$dir" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \) | head -n "$TARGET" | xargs -I {} cp {} "$DEST/$cat_name/"
    else
        echo "Not enough images. Copying all ($count) and augmenting..."
        # On copie tout le contenu du dossier source vers la destination
        cp "$dir"/* "$DEST/$cat_name/" 2>/dev/null

        needed=$((TARGET - count))
        # Chaque run d'Augmentation.py crée 6 images
        runs=$(( (needed + 5) / 6 ))

        # On récupère la liste des fichiers copiés pour l'augmentation
        mapfile -t to_augment < <(find "$DEST/$cat_name" -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" \))
        num_to_augment=${#to_augment[@]}

        if [ "$num_to_augment" -gt 0 ]; then
            echo "Starting $runs augmentations..."
            for ((i=0; i<runs; i++)); do
                idx=$((i % num_to_augment))
                target_file="${to_augment[$idx]}"

                # Lancement de l'augmentation en arrière-plan
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