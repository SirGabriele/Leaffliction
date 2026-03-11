from pathlib import Path
from PIL import Image, UnidentifiedImageError

import numpy as np


def load_image(image_path: Path) -> np.ndarray:
    try:
        with Image.open(image_path) as img:
            if img.format.upper() not in ["PNG", "JPEG", ]:
                raise AssertionError(
                    "Only formats accepted are PNG, JPG, and JPEG"
                )

            image = np.array(img)
    except UnidentifiedImageError:
        raise AssertionError("Only formats accepted are PNG, JPG, and JPEG")

    return image
