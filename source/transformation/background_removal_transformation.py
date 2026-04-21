import numpy as np
import cv2

def background_removal_transformation(image: np.ndarray, final_mask: np.ndarray) -> np.ndarray:
    mask_rgb = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2RGB)
    return cv2.bitwise_and(image, mask_rgb)