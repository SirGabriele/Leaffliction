import numpy as np
from plantcv import plantcv


def gaussian_blur(image: np.ndarray) -> np.ndarray:
    return plantcv.gaussian_blur(img=image, ksize=(9, 9))
