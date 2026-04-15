import cv2
import numpy as np


def saturation_transformation(image: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    return hsv[:, :, 1]
