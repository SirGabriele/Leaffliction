import json
from pathlib import Path
import tensorflow as tf
import argparse
import shutil
import os
from typing import Tuple
from tensorflow.keras import Sequential, layers

from source.utils.existing_directory import existing_directory
from Transformation import handle_batch_mode

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
DENSE_UNITS = 128
CONV_FILTERS = (32, 64, 128)
AUGMENTED_DIR = "transformation_images"

def _transform_and_load_dataset(dataset_path: Path) -> Tuple[tf.data.Dataset, tf.data.Dataset]:
    #handle_batch_mode(dataset_path, Path(AUGMENTED_DIR), {"background_removal": True})
    return [
        tf.keras.utils.image_dataset_from_directory(
        AUGMENTED_DIR,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    ),
     tf.keras.utils.image_dataset_from_directory(
        AUGMENTED_DIR,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    )]

def _build_model(class_names) -> Sequential:
    shape = (IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
    model = Sequential()

    model.add(layers.Input(shape))
    model.add(layers.Rescaling(1.0 / 255))

    model.add(layers.Conv2D(CONV_FILTERS[0], (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(CONV_FILTERS[1], (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Conv2D(CONV_FILTERS[2], (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(layers.Flatten())
    model.add(layers.Dense(DENSE_UNITS, activation='relu'))

    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(len(class_names), activation='softmax'))

    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    return model


def _save_and_zip(model, class_names, augmented_dir):
    export = Path("leaffliction_results")
    export.mkdir(exist_ok=True)

    model.save(export / "leaf_model.keras")

    with open(export / "class_names.json", "w") as f:
        json.dump(class_names, f)

    dest_img_dir = export / "augmented_directory"
    if dest_img_dir.exists():
        shutil.rmtree(dest_img_dir)
    shutil.copytree(augmented_dir, dest_img_dir)
    shutil.make_archive("training_results", "zip", export)
    shutil.rmtree(export)


def train(images_folder: Path):
    train_ds, val_ds = _transform_and_load_dataset(images_folder)

    class_names = train_ds.class_names

    model = _build_model(class_names)
    model.summary()

    print("Model compiled successfully!\n")
    print('=' * 50)
    print("\nTraining...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=30
    )
    with open("class_names.json", "w") as f:
        json.dump(class_names, f)
    model.save("leaf_model.keras")
    _save_and_zip(model, class_names, AUGMENTED_DIR)
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


def main():
    args = argparse_init().parse_args()
    train(args.directory)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(err)


