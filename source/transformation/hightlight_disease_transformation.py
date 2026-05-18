import cv2
import numpy as np


def highlight_disease_transformation(image: np.ndarray,
                                     final_mask: np.ndarray) -> np.ndarray:
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    lower_disease1 = np.array([0, 40, 40])
    upper_disease1 = np.array([35, 255, 255])
    mask_1 = cv2.inRange(hsv, lower_disease1, upper_disease1)

    lower_disease2 = np.array([160, 40, 40])
    upper_disease2 = np.array([179, 255, 255])
    mask_2 = cv2.inRange(hsv, lower_disease2, upper_disease2)

    disease_color_mask = cv2.bitwise_or(mask_1, mask_2)

    disease_mask = cv2.bitwise_and(disease_color_mask, final_mask)

    result_image = image.copy()

    neon_green = [57, 255, 20]
    result_image[disease_mask == 255] = neon_green
    result_image[final_mask == 0] = [0, 0, 0]

    return result_image
