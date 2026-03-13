import cv2
import numpy as np


def edge_detection(image: np.ndarray) -> np.ndarray:
    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])

    result = cv2.filter2D(image, -1, kernel)
    return result
