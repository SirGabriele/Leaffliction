import json
import multiprocessing
import shutil
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path
import tensorflow as tf
import argparse
from typing import Tuple
from tensorflow.keras import Sequential, layers

from config import AUGMENTED_DIR, IMAGE_SIZE, BATCH_SIZE, DENSE_UNITS, \
    CONV_FILTERS, BALANCED_DIR
from source.augment_image import augment_image
from source.utils.existing_directory import existing_directory
from Transformation import handle_batch_mode


def _transform_and_load_dataset(dataset_path: Path) -> Tuple[tf.data.Dataset, tf.data.Dataset]:
    handle_batch_mode(dataset_path, Path(AUGMENTED_DIR), {"background_removal": True})
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


def _balance_dataset(images_folder: Path) -> Path:
    TARGET = 2000
    Path(BALANCED_DIR).mkdir(parents=True, exist_ok=True)

    for cat_dir in images_folder.iterdir():
        if not cat_dir.is_dir():
            continue

        cat_name = cat_dir.name
        dest_dir = Path(BALANCED_DIR) / cat_name
        dest_dir.mkdir(parents=True, exist_ok=True)

        images = [f for f in cat_dir.iterdir() if
                  f.is_file() and f.suffix.lower() in {'.jpg', '.jpeg',
                                                       '.png'}]
        count = len(images)

        print(f"--- Category: {cat_name} ({count} images) ---")

        if count >= TARGET:
            print(f"Too many or enough images. Copying first {TARGET}...")
            for img in images[:TARGET]:
                shutil.copy2(img, dest_dir / img.name)
        else:
            print(
                f"Not enough images. Copying all ({count}) and augmenting...")
            copied_images = []
            for img in images:
                dest_file = dest_dir / img.name
                shutil.copy2(img, dest_file)
                copied_images.append(dest_file)

            needed = TARGET - count
            runs = (needed + 5) // 6

            num_to_augment = len(copied_images)
            if num_to_augment > 0:
                print(f"Starting {runs} augmentations...")
                tasks = [copied_images[i % num_to_augment] for i in
                         range(runs)]

                with ProcessPoolExecutor(
                        max_workers=multiprocessing.cpu_count()) as executor:
                    executor.map(augment_image, tasks)

    print(f"--- Done! Check the '{BALANCED_DIR}' folder. ---")
    return Path(BALANCED_DIR)


def train(images_folder: Path):
    balanced_images_folder = _balance_dataset(images_folder)
    train_ds, val_ds = _transform_and_load_dataset(balanced_images_folder)

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
    train(Path(args.directory))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(err)


