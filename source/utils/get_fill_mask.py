import numpy as np

from plantcv import plantcv


def get_fill_mask(image: np.ndarray) -> np.ndarray:
    a_channel = plantcv.rgb2gray_lab(rgb_img=image, channel='a')
    mask = plantcv.threshold.otsu(gray_img=a_channel, object_type="dark")
    mask_clean = plantcv.fill(bin_img=mask, size=50)

    return mask_clean
