import cv2
import numpy as np


def edge_detection(final_mask: np.ndarray) -> np.ndarray:
    return cv2.Canny(final_mask, 100, 200)
