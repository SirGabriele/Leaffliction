import cv2
import numpy as np

from pathlib import Path
from config import FLIP_ROTATION_AXIS
from source.generate_augmented_file_name import generate_augmented_file_name
from source.save_image import save_image_in_augmented_directory


def flip(augmented_directory: Path, image_file_path: Path,
         image: np.ndarray) -> np.ndarray:
    flipped_image: np.ndarray = cv2.flip(image, FLIP_ROTATION_AXIS)

    image_file_path: Path = generate_augmented_file_name(
        image_file_path,
        filter_suffix="Flip"
    )

    save_image_in_augmented_directory(
        augmented_directory, image_file_path, flipped_image
    )

    return flipped_image
