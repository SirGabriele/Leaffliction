import numpy as np

from plantcv import plantcv


def get_fill_mask(image: np.ndarray) -> np.ndarray:
    a_channel = plantcv.rgb2gray_lab(rgb_img=image, channel='a')
    mask = plantcv.threshold.otsu(gray_img=a_channel, object_type="dark")
    mask_clean = plantcv.fill(bin_img=mask, size=50)

    return mask_clean
    # image_without_background = rembg.remove(image)

    # Grayscale image of the light colorspace channel
    # image_grayscale = plantcv.rgb2gray_lab(
    #     rgb_img=image_without_background, channel='l'
    # )

    # Binary mask on threshold values targeting light objects
    # return plantcv.threshold.otsu(
    #     gray_img=image_grayscale, object_type="light"
    # )
