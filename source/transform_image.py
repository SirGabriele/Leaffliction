import argparse
import math
import numpy as np

from pathlib import Path
from matplotlib import pyplot as plt
from source.load_image import load_image
from source.transformation.analyze import analyze
from source.transformation.gaussian_blur import gaussian_blur
from source.transformation.generate_histogram import generate_histogram
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


def transform_image(image: np.ndarray, args: argparse.Namespace) -> dict[str, np.ndarray]:

    fill_mask = get_fill_mask(image)

    do_all = not any([
        args.blur,
        args.mask,
        args.roi,
        args.analysis,
        args.pseudolandmark,
        args.color_histogram
    ])

    transformed_imgs: dict[str, np.ndarray] = {}

    if do_all or args.blur:
        transformed_imgs["Gaussian blur"] = gaussian_blur(image)
    if do_all or args.mask:
        transformed_imgs["Mask"] = fill_mask
    if do_all or args.roi or args.analyze:
        roi, disease_mask = region_of_interest(image, fill_mask)
        if do_all or args.roi:
            transformed_imgs["ROI"] = roi
        if do_all or args.analysis:
            transformed_imgs["Analysis"] = analyze(image, disease_mask)
    if do_all or args.pseudolandmark:
        transformed_imgs["Pseudolandmark"] = pseudolandmark(image, fill_mask)
    if do_all or args.color_histogram:
        transformed_imgs["Color Histogram"] = generate_histogram(image, fill_mask)
    return transformed_imgs


