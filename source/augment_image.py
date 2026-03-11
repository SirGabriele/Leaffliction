import inspect

import numpy as np

from matplotlib import pyplot as plt
from pathlib import Path

from source.create_augmented_directory import create_augmented_directory
from source.filters.blur import blur
from source.filters.flip import flip
from source.filters.scale import scale
from source.load_image import load_image


# TODO Delete this function
def display_images(image, blurred_image, flipped_image, scaled_image):
    nb_images_to_display = len(inspect.signature(display_images).parameters)
    plt.subplot(1, nb_images_to_display, 1)
    plt.imshow(image)
    plt.title("Original image")
    plt.axis("off")

    plt.subplot(1, nb_images_to_display, 2)
    plt.imshow(blurred_image)
    plt.title("Blurred image")
    plt.axis("off")

    plt.subplot(1, nb_images_to_display, 3)
    plt.imshow(flipped_image)
    plt.title("Flipped image")
    plt.axis("off")

    plt.subplot(1, nb_images_to_display, 4)
    plt.imshow(scaled_image)
    plt.title("Scale image")
    plt.axis("off")

    plt.show()


def augment_image(image_file_path: Path):
    # Creates the augmented directory that match the image file path
    augmented_directory: Path = create_augmented_directory(image_file_path)

    # Loads the image data
    image: np.ndarray = load_image(image_file_path)

    # Applies filters
    blurred_image: np.ndarray = blur(augmented_directory, image_file_path, image)
    flipped_image: np.ndarray = flip(augmented_directory, image_file_path, image)
    scaled_image = scale(augmented_directory, image_file_path, image)

    display_images(image, blurred_image, flipped_image, scaled_image)
