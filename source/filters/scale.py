import cv2
import numpy as np

from pathlib import Path
from config import SCALE_FACTOR
from source.generate_augmented_file_name import generate_augmented_file_name
from source.save_image import save_filtered_image


def scale(augmented_directory: Path, image_file_path: Path,
          image: np.ndarray) -> np.ndarray:
    # Scales the image and then crops the resulting image to obtain an image
    # the size of the original one
    scaled_image = cv2.resize(
        image,
        dsize=None,
        fx=SCALE_FACTOR,
        fy=SCALE_FACTOR,
        interpolation=cv2.INTER_CUBIC
    )

    original_h, original_w = image.shape[:2]
    scaled_h, scaled_w = scaled_image.shape[:2]

    # Handles zoom in
    if SCALE_FACTOR > 1:
        crop_start_idx_h = (scaled_h - original_h) // 2
        crop_start_idx_w = (scaled_w - original_w) // 2

        cropped_image = scaled_image[
            crop_start_idx_h:crop_start_idx_h + original_h,
            crop_start_idx_w:crop_start_idx_w + original_w
        ]
    # Handles zoom out
    else:
        # Creates a black image with the same size as the original
        cropped_image = np.zeros_like(image)

        crop_start_idx_h = (original_h - scaled_h) // 2
        crop_start_idx_w = (original_w - scaled_w) // 2

        # Fills this black image with the down scaled original image
        cropped_image[
            crop_start_idx_h:crop_start_idx_h + scaled_h,
            crop_start_idx_w:crop_start_idx_w + scaled_w
        ] = scaled_image

    image_file_path: Path = generate_augmented_file_name(
        image_file_path,
        filter_suffix="Scale"
    )

    save_filtered_image(augmented_directory, image_file_path, cropped_image)

    return cropped_image
