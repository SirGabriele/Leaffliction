import argparse
import math
import numpy as np

from pathlib import Path
from matplotlib import pyplot as plt
from source.transformation.analyze import analyze
from source.transformation.edges_detection import edge_detection
from source.transformation.saturation import saturation
from source.transformation.generate_histogram import generate_histogram
from source.transformation.hightlight_disease import highlight_disease
from source.transformation.pseudolandmark import pseudolandmark
from source.transformation.region_of_interest import region_of_interest


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
        if img.ndim == 2:
            plt.set_cmap("gray")
        plt.subplot(nb_rows, nb_cols, i)
        plt.imshow(img)
        plt.title(title)
        plt.axis("off")

    plt.tight_layout()
    plt.show()


def transform_image(image: np.ndarray, args: argparse.Namespace) -> dict[str, np.ndarray]:

    roi_mask = region_of_interest(image)
    do_all = not any([
        args.saturation,
        args.mask,
        args.roi,
        args.analysis,
        args.pseudolandmark,
        args.edges,
    ])

    transformed_imgs: dict[str, np.ndarray] = {}

    if do_all or args.mask:
        transformed_imgs["Mask"] = roi_mask
    if do_all or args.saturation:
        transformed_imgs["Saturation"] = saturation(image)
    if do_all or args.roi or args.analysis:
        if do_all or args.roi:
            transformed_imgs["ROI (Disease highlight)"] = highlight_disease(image, roi_mask)
        if do_all or args.analysis:
            transformed_imgs["Analysis"] = analyze(image, roi_mask)
    if do_all or args.pseudolandmark:
        transformed_imgs["Pseudolandmark"] = pseudolandmark(image, roi_mask)
    if do_all or args.edges:
        transformed_imgs["Edges"] = edge_detection(roi_mask)
    return transformed_imgs



