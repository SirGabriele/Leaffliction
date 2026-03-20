import numpy as np

from plantcv import plantcv
from source.utils.remove_background import remove_background


def get_fill_mask(image: np.ndarray) -> np.ndarray:
    image_without_background = remove_background(image)

    # Grayscale image of the light colorspace channel
    image_grayscale = plantcv.rgb2gray_lab(
        rgb_img=image_without_background, channel='l'
    )

    # Binary mask on threshold values targeting light objects
    return plantcv.threshold.otsu(
        gray_img=image_grayscale, object_type="light"
    )
