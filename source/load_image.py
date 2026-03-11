import numpy as np

from pathlib import Path
from PIL import Image, UnidentifiedImageError


def load_image(image_path: Path) -> np.ndarray:
    try:
        with Image.open(image_path) as img:
            if img.format.lower() != "jpeg":
                raise AssertionError(
                    "Only format accepted is JPEG/JPG"
                )

            image = np.array(img)
    except UnidentifiedImageError:
        raise AssertionError("Only format accepted is JPEG/JPG")

    return image
