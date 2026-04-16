import cv2
import numpy as np

from plantcv import plantcv


def pseudolandmark_transformation(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    top_pts, bottom_pts, center_pts = plantcv.homology.x_axis_pseudolandmarks(
        img=image, mask=mask, label='default'
    )

    # Lowers the array by one dimension
    # From [[[x1, y1]], [[x,2 y2]], [[x3, y3]]]
    # To [[x1, y1], [x2, y2], [x3, y3]]
    top_pts = np.squeeze(top_pts)
    bottom_pts = np.squeeze(bottom_pts)
    center_pts = np.squeeze(center_pts)

    image_copy = image.copy()

    for x, y in top_pts:
        cv2.circle(image_copy, (int(x), int(y)), 4, (255, 0, 0), -1)
    for x, y in bottom_pts:
        cv2.circle(image_copy, (int(x), int(y)), 4, (0, 255, 0), -1)
    for x, y in center_pts:
        cv2.circle(image_copy, (int(x), int(y)), 4, (0, 0, 255), -1)
    return image_copy
