import contextlib
import os

import cv2
import numpy as np

from plantcv import plantcv


def pseudolandmark(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    # skeleton = plantcv.morphology.skeletonize(mask=mask)
    # segments, segment_objects = plantcv.morphology.segment_skeleton(
    #     skel_img=skeleton)
    # # device, top, bottom, center_v = plantcv.x_axis_pseudolandmarks(mask, image)
    # return segments

    # win = 24
    # thresh = 90
    # image_copy = image.copy()

    # with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    #     homolog_pts, start_pts, stop_pts, ptvals, chain, max_dist = (
    #         plantcv.homology.acute(
    #             img=image_copy,
    #             mask=mask, win=win,
    #             threshold=thresh))
    #
    # homolog_pts = np.squeeze(homolog_pts)
    #
    # for x, y in homolog_pts:
    #     cv2.circle(image_copy, (x, y), 4, (255, 0, 0), -1)

    # return image_copy

    image_copy = image.copy()
    top_pts, bottom_pts, center_pts = plantcv.homology.x_axis_pseudolandmarks(
        img=image, mask=mask, label='default'
    )
    # print(top_pts)
    top_pts = np.array(top_pts).reshape(-1, 2)
    bottom_pts = np.array(bottom_pts).reshape(-1, 2)
    center_pts = np.array(center_pts).reshape(-1, 2)
    for x, y in top_pts:
        cv2.circle(image_copy, (int(x), int(y)), 4, (255, 0, 0), -1)
    for x, y in bottom_pts:
        cv2.circle(image_copy, (int(x), int(y)), 4, (0, 255, 0), -1)
    for x, y in center_pts:
        cv2.circle(image_copy, (int(x), int(y)), 4, (0, 0, 255), -1)
    return image_copy