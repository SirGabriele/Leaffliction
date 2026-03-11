import numpy as np

from matplotlib import pyplot as plt
from pathlib import Path

from config import DISPLAY_AUGMENTED_IMAGES
from source.create_augmented_directory import create_augmented_directory
from source.filters.blur import blur
from source.filters.flip import flip
from source.filters.illuminate import illuminate
from source.filters.rotate import rotate
from source.filters.scale import scale
from source.load_image import load_image


def display_images(original_img: np.ndarray, blur_img: np.ndarray,
                   flip_img: np.ndarray, scale_img: np.ndarray,
                   rotate_img: np.ndarray, illuminate_img: np.ndarray):
    images = [original_img, blur_img, flip_img, scale_img, rotate_img, illuminate_img]
    titles = ["Original", "Blur", "Flip", "Scale", "Rotate", "Illuminate"]

    nb_rows = 2
    nb_cols = 3

    plt.figure(figsize=(12, 6))

    for i, (img, title) in enumerate(zip(images, titles), start=1):
        plt.subplot(nb_rows, nb_cols, i)
        plt.imshow(img)
        plt.title(title)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


def augment_image(image_file_path: Path):
    # Creates the augmented directory that match the image file path
    augmented_directory: Path = create_augmented_directory(image_file_path)

    # Loads the image data
    image: np.ndarray = load_image(image_file_path)

    # Applies filters
    blurred_image: np.ndarray = blur(augmented_directory, image_file_path, image)
    flipped_image: np.ndarray = flip(augmented_directory, image_file_path, image)
    scaled_image: np.ndarray = scale(augmented_directory, image_file_path, image)
    rotated_image: np.ndarray = rotate(augmented_directory, image_file_path, image)
    illuminated_image: np.ndarray = illuminate(
        augmented_directory, image_file_path, image
    )

    if DISPLAY_AUGMENTED_IMAGES:
        display_images(
            original_img=image,
            blur_img=blurred_image,
            flip_img=flipped_image,
            scale_img=scaled_image,
            rotate_img=rotated_image,
            illuminate_img=illuminated_image
        )
