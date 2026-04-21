import json
import random
import time
from pathlib import Path

import tensorflow as tf
from Transformation import handle_batch_mode
from source.load_image import load_image
from source.transform_image import transform_image
from source.augment_image import augment_image
from source.count_images import count_images
from source.transformation.roi_transformation import roi_transformation
from tensorflow.keras import Sequential, layers
import argparse
from source.utils.existing_directory import existing_directory
import cv2
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
import shutil
import os


def save_and_zip(model, class_names, augmented_dir):
    print("\n[ZIP] Préparation de l'archive finale...")

    # 1. Créer un dossier temporaire pour regrouper les éléments
    export_path = "leaffliction_results"
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    # 2. Sauvegarder le modèle et les classes dedans
    model.save(f"{export_path}/leaf_model.keras")

    import json
    with open(f"{export_path}/class_names.json", "w") as f:
        json.dump(class_names, f)

    # 3. Copier le dossier des images augmentées dans notre dossier d'export
    # On vérifie si le dossier existe déjà pour éviter une erreur
    dest_img_dir = f"{export_path}/augmented_directory"
    if os.path.exists(dest_img_dir):
        shutil.rmtree(dest_img_dir)
    shutil.copytree(augmented_dir, dest_img_dir)

    # 4. Créer le ZIP à partir du dossier d'export
    shutil.make_archive("training_results", 'zip', export_path)

    # 5. Optionnel : supprimer le dossier temporaire pour faire propre
    shutil.rmtree(export_path)

    print("Archive 'training_results.zip' créée avec succès !")

def balance_image_distribution(images: Path):
    count_images_dir = count_images(images).items()
    max_val: int = max(count_images(images).values())
    if max_val < 1000 :
        max_val = 1000
    for directory in count_images_dir:
        nb_images_directory = directory[1]
        subdir_path = images / directory[0]
        image_files = [f for f in subdir_path.iterdir() if f.is_file()]
        for img in image_files:
            if nb_images_directory == max_val:
                break
            augment_image(img, display=False)
            nb_images_directory += 6

def train(images_folder):
    #handle_batch_mode(Path("train_images"), Path("transformation_images"), {"background_removal": True})
    image_size = (128, 128)
    batch_size = 32
    shape = (image_size[0], image_size[1], 3)

    train_ds = tf.keras.utils.image_dataset_from_directory(
       "transformation_images",
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=image_size,
        batch_size=batch_size
    )
    print("Training dataset loaded successfully!\n")
    print("Loading validation dataset...")

    val_ds = tf.keras.utils.image_dataset_from_directory(
        "transformation_images",
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=image_size,
        batch_size=batch_size
    )
    chemin_image_test = val_ds.file_paths

    print(f"L'image parfaite pour ton test est ici : {chemin_image_test}")

    print("Validation dataset loaded successfully!\n")
    print("="*50)

    class_names = train_ds.class_names
    print("\nClasses détectées :", class_names)


    model = Sequential()
    model.add(layers.Input(shape))
    model.add(layers.Rescaling(1.0 / 255))

    model.add(layers.Conv2D(32, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(128, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))

    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(len(class_names), activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    print("Model compiled successfully!\n")
    print('='*50)
    print("\nTraining...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=5
    )
    class_names = train_ds.class_names
    with open("class_names.json", "w") as f:
        json.dump(class_names, f)
    model.save("leaf_model.keras")
    #save_and_zip(model, class_names, "augmented_directory")
    print("Training completed!")
    print('='*50)
    print('\nSummary :')
    print("\nFinal training accuracy: {:.2f}%".format(history.history['accuracy'][-1] * 100))
    print("Final validation accuracy: {:.2f}%".format(history.history['val_accuracy'][-1] * 100))

def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run training',
        usage="python3.13 train.py <directory>"
    )
    parser.add_argument(
        'directory',
        type=existing_directory,
        help='Path to the directory file'
    )
    return parser

def main() :
    args = argparse_init().parse_args()
    train(args.directory)
    exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(err)
