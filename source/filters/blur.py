import cv2
import numpy as np

from pathlib import Path

from config import BLUR_KERNEL_SIZE
from source.generate_augmented_file_name import generate_augmented_file_name
from source.save_image import save_filtered_image


def blur(augmented_directory: Path, image_file_path: Path, image: np.ndarray) -> (
        np.ndarray):
    blurred_image: np.ndarray = cv2.blur(image, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE))

    image_file_path: Path = generate_augmented_file_name(
        image_file_path,
        filter_suffix="Blur"
    )

    # Saves the filtered image in the augmented directory
    save_filtered_image(augmented_directory, image_file_path, blurred_image)

    return blurred_image
