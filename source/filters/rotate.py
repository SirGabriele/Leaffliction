import cv2
import numpy as np

from pathlib import Path
from config import ROTATION_ANGLE
from source.generate_augmented_file_name import generate_augmented_file_name
from source.save_image import save_filtered_image


def rotate(augmented_directory: Path, image_file_path: Path,
           image: np.ndarray) -> np.ndarray:
    height, width = image.shape[:2]
    center = (width // 2, height // 2)

    rotation_matrix = cv2.getRotationMatrix2D(center, ROTATION_ANGLE, 1.0)

    rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    image_file_path: Path = generate_augmented_file_name(
        image_file_path,
        filter_suffix="Rotate"
    )

    save_filtered_image(augmented_directory, image_file_path, rotated_image)

    return rotated_image
