import math

import numpy as np

from matplotlib import pyplot as plt
from pathlib import Path

from config import DISPLAY_AUGMENTED_IMAGES
from source.create_augmented_directory import create_augmented_directory
from source.filters.blur import blur
from source.filters.project import project
from source.filters.flip import flip
from source.filters.illuminate import illuminate
from source.filters.rotate import rotate
from source.filters.scale import scale
from source.load_image import load_image


def display_images(original_img: np.ndarray,
                   augmented_imgs: dict[str, np.ndarray]) -> None:
    # Displays 3 images per rows, plus one row for the original image
    nb_cols = 3
    nb_rows = len(augmented_imgs) // nb_cols + 1
    second_row_first_column_idx = nb_cols + 1

    plt.figure(num="Augmented images")

    # Places original image in the middle of the first row
    plt.subplot(
        nb_rows, nb_cols, math.ceil(len(augmented_imgs) / nb_cols)
    )
    plt.imshow(original_img)
    plt.title("Original")
    plt.axis("off")

    for i, (title, img) in enumerate(
            augmented_imgs.items(), start=second_row_first_column_idx
    ):
        plt.subplot(nb_rows, nb_cols, i)
        plt.imshow(img)
        plt.title(title)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


def augment_image(image_file_path: Path):
    augmented_directory: Path = create_augmented_directory(image_file_path)

    image: np.ndarray = load_image(image_file_path)

    augmented_imgs: dict[str, np.ndarray] = {
        "Blur": blur(augmented_directory, image_file_path, image),
        "Flip": flip(augmented_directory, image_file_path, image),
        "Scaling": scale(augmented_directory, image_file_path, image),
        "Rotation": rotate(augmented_directory, image_file_path, image),
        "Illumination": illuminate(augmented_directory, image_file_path,
                                   image),
        "Projection": project(augmented_directory, image_file_path, image)
    }

    if DISPLAY_AUGMENTED_IMAGES:
        display_images(original_img=image, augmented_imgs=augmented_imgs)
