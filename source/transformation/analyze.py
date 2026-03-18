import numpy as np
from plantcv import plantcv


def analyze(image: np.ndarray, fill_mask: np.ndarray) -> np.ndarray:
    return plantcv.analyze.size(img=image, labeled_mask=fill_mask)
