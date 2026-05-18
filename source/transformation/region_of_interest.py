import cv2
import numpy as np


def region_of_interest(image: np.ndarray, fill_mask: np.ndarray) \
        -> tuple[np.ndarray, np.ndarray]:
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    lower_green = np.array([36, 0, 0])
    upper_green = np.array([80, 255, 255])

    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_mask = cv2.medianBlur(green_mask, 5)

    contours, _ = cv2.findContours(
        fill_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    plant_contour = max(contours, key=cv2.contourArea)

    roi_mask = np.zeros_like(fill_mask)
    cv2.drawContours(roi_mask, [plant_contour], -1, 255, -1)
    disease_mask = cv2.bitwise_and(roi_mask, cv2.bitwise_not(green_mask))

    image_copy = image.copy()

    # Sets all pixels that do not match the green mask to black
    black = [0, 0, 0]
    image_copy[green_mask == 0] = black

    # Sets all pixels that do not match the green mask but match the ROI mask
    # to neon green
    neon_green = [57, 255, 20]
    image_copy[disease_mask == 255] = neon_green
    return image_copy, disease_mask
