from pathlib import Path

import cv2
import numpy as np


def save_filtered_image(augmented_directory: Path, image_file_path: Path,
                        filtered_image: np.ndarray) -> None:
    # We use Pillow to open the image, which channel order is RGB.
    # However, OpenCV uses BGR, so we have to convert the image data to BGR before
    # saving it
    cv2.imwrite(
        str(augmented_directory / image_file_path.name),
        cv2.cvtColor(filtered_image, cv2.COLOR_RGB2BGR)
    )
