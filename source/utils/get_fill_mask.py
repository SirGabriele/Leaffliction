import numpy as np
import rembg

from plantcv import plantcv


def get_fill_mask(image: np.ndarray) -> np.ndarray:
    image_without_background = rembg.remove(image)

    # Grayscale image of the light colorspace channel
    image_grayscale = plantcv.rgb2gray_lab(
        rgb_img=image_without_background, channel='l'
    )

    # Binary mask on threshold values targeting light objects
    return plantcv.threshold.otsu(
        gray_img=image_grayscale, object_type="light"
    )
