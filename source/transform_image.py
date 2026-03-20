import math
import numpy as np

from pathlib import Path
from matplotlib import pyplot as plt
from source.load_image import load_image
from source.transformation.analyze import analyze
from source.transformation.gaussian_blur import gaussian_blur
from source.transformation.pseudolandmark import pseudolandmark
from source.transformation.region_of_interest import region_of_interest
from source.utils.get_fill_mask import get_fill_mask


def display_images(original_img: np.ndarray,
                   transformed_imgs: dict[str, np.ndarray]) -> None:
    # Displays 3 images per rows, plus one row for the original image
    nb_cols = 3
    nb_rows = 1 + math.ceil(len(transformed_imgs) / nb_cols)
    middle_column_index = 1 + math.ceil(nb_cols // 2)
    second_row_first_column_idx = nb_cols + 1

    plt.figure(num="Transformed images")

    # Places original image in the middle of the first row
    plt.subplot(nb_rows, nb_cols, middle_column_index)
    plt.imshow(original_img)
    plt.title("Original")
    plt.axis("off")

    for i, (title, img) in enumerate(
            transformed_imgs.items(), start=second_row_first_column_idx
    ):
        plt.subplot(nb_rows, nb_cols, i)
        plt.imshow(img)
        plt.title(title)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


def transform_image(image_file_path: Path) -> None:
    image: np.ndarray = load_image(image_file_path)

    fill_mask = get_fill_mask(image)
    roi, disease_mask = region_of_interest(image, fill_mask)

    transformed_imgs: dict[str, np.ndarray] = {
        "Gaussian blur": gaussian_blur(image),
        "ROI": roi,
        "Analysis": analyze(image, disease_mask),
        "pseudolandmark": pseudolandmark(image, fill_mask)
    }

    display_images(image, transformed_imgs)
