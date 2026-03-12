import cv2
import numpy as np

from pathlib import Path
from config import PROJECTION_TOP_LEFT_FACTORS
from config import PROJECTION_TOP_RIGHT_FACTORS
from config import PROJECTION_BOTTOM_LEFT_FACTORS
from config import PROJECTION_BOTTOM_RIGHT_FACTORS
from source.generate_augmented_file_name import generate_augmented_file_name
from source.save_image import save_image_in_augmented_directory


def project(augmented_directory: Path, image_file_path: Path,
            image: np.ndarray) -> np.ndarray:
    y_max, x_max = image.shape[:2]

    # The (x, y) source coordinates of the image's corners. In order: top-left,
    # top-right, bottom-right, bottom-left
    corners_src_coord: np.ndarray = np.float32([
        [0, 0],
        [x_max - 1, 0],
        [x_max - 1, y_max - 1],
        [0, y_max - 1]
    ])

    tl_x_factor, tl_y_factor = PROJECTION_TOP_LEFT_FACTORS
    tr_x_factor, tr_y_factor = PROJECTION_TOP_RIGHT_FACTORS
    br_x_factor, br_y_factor = PROJECTION_BOTTOM_RIGHT_FACTORS
    bl_x_factor, bl_y_factor = PROJECTION_BOTTOM_LEFT_FACTORS

    # The (x, y) destination coordinates of the image's corners
    corners_dst_coord = np.float32([
        [x_max * tl_x_factor, y_max * tl_y_factor],
        [x_max * tr_x_factor, y_max * tr_y_factor],
        [x_max * br_x_factor, y_max * br_y_factor],
        [x_max * bl_x_factor, y_max * bl_y_factor]
    ])

    transformation_matrix = cv2.getPerspectiveTransform(
        corners_src_coord, corners_dst_coord
    )

    projected_img = cv2.warpPerspective(
        image, transformation_matrix, (x_max, y_max)
    )

    image_file_path: Path = generate_augmented_file_name(
        image_file_path,
        filter_suffix="Projection"
    )

    save_image_in_augmented_directory(
        augmented_directory, image_file_path, projected_img
    )

    return projected_img
