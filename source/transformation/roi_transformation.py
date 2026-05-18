import cv2
import numpy as np
from plantcv import plantcv as pcv


def roi_transformation(image: np.ndarray, iterations: int = 5,
                       margin: int = 20) -> np.ndarray:
    h, w = image.shape[:2]

    # We suppose that the leaf is in the center, we take a rectangle
    # with a margin.
    rect = (margin, margin, w - (2 * margin), h - (2 * margin))

    # Internal masks used by GrabCut, they are initialized as zeros and
    # updated by the algorithm.
    background_mask = np.zeros((1, 65), np.float64)
    foreground_mask = np.zeros((1, 65), np.float64)

    mask = np.zeros((h, w), np.uint8)
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    cv2.grabCut(img_bgr, mask, rect, background_mask, foreground_mask,
                iterations, cv2.GC_INIT_WITH_RECT)

    # GrabCut modify the 'mask' with 4 values :
    # 0: Definite Background, 1: Definite Foreground, 2: Probable Background,
    # 3: Probable Foreground
    # We want foreground (1 and 3)
    bin_mask = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)

    # GrabCut can leave small isolated background points. We use pcv.fill to
    # remove noise smaller than
    # X pixels (e.g., 100) and pcv.fill_holes to fill small holes in the leaf.
    cleaned_mask = pcv.fill(bin_img=bin_mask, size=100)
    final_mask = pcv.fill_holes(bin_img=cleaned_mask)
    return final_mask
