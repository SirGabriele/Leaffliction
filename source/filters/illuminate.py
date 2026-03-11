import cv2
import numpy as np

from pathlib import Path

from config import ILLUMINATE_ALPHA, ILLUMINATE_BETA
from source.generate_augmented_file_name import generate_augmented_file_name
from source.save_image import save_filtered_image


def illuminate(augmented_directory: Path, image_file_path: Path, image: np.ndarray) \
        -> np.ndarray:
    # new_pixel = alpha ∗ old_pixel + beta
    illuminated_image = cv2.convertScaleAbs(
        image,
        alpha=ILLUMINATE_ALPHA,
        beta=ILLUMINATE_BETA
    )

    image_file_path: Path = generate_augmented_file_name(
        image_file_path,
        filter_suffix="Illuminate"
    )

    # Saves the filtered image in the augmented directory
    save_filtered_image(augmented_directory, image_file_path, illuminated_image)

    return illuminated_image
