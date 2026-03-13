import cv2
import numpy as np


def gaussian_blur(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)

    # blurred_image: np.ndarray = cv2.GaussianBlur(image, (9, 9), 0)
    # blurred_image: np.ndarray = plantcv.gaussian_blur(image, (9, 9), 0)
    # _, bw = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    bw = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)

    return bw
