import math
import numpy as np

from matplotlib import pyplot as plt
from source.transformation.analyze_transformation import analyze_transformation
from source.transformation.edges_detection_transformation import \
    edge_detection_transformation
from source.transformation.saturation_transformation import \
    saturation_transformation
from source.transformation.hightlight_disease_transformation import \
    highlight_disease_transformation
from source.transformation.pseudolandmark_transformation import \
    pseudolandmark_transformation
from source.transformation.roi_transformation import roi_transformation
from source.transformation.background_removal_transformation import \
    background_removal_transformation


def display_images(original_img: np.ndarray,
                   transformed_imgs: dict[str, np.ndarray]) -> None:
    # Displays 3 images_dir per rows, plus one row for the original image
    nb_cols = 3
    nb_rows = 1 + math.ceil(len(transformed_imgs) / nb_cols)
    middle_column_index = 1 + math.ceil(nb_cols // 2)
    second_row_first_column_idx = nb_cols + 1

    plt.figure(num="Transformed images_dir")

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


def transform_image(
        image: np.ndarray,
        saturation: bool = False,
        mask: bool = False,
        roi: bool = False,
        analysis: bool = False,
        pseudolandmark: bool = False,
        edges: bool = False,
        background_removal: bool = False,
) -> dict[str, np.ndarray]:
    roi_mask = roi_transformation(image)
    do_all = not any([
        saturation,
        mask,
        roi,
        analysis,
        pseudolandmark,
        edges,
        background_removal
    ])

    transformed_imgs: dict[str, np.ndarray] = {}

    if do_all or mask:
        transformed_imgs["Mask"] = roi_mask
    if do_all or background_removal:
        transformed_imgs[
            "Background removal"] = background_removal_transformation(image,
                                                                      roi_mask)
    if do_all or saturation:
        transformed_imgs["Saturation"] = saturation_transformation(image)
    if do_all or roi or analysis:
        if do_all or roi:
            transformed_imgs[
                "ROI (Disease highlight)"] = highlight_disease_transformation(
                image, roi_mask)
        if do_all or analysis:
            transformed_imgs["Analysis"] = analyze_transformation(image,
                                                                  roi_mask)
    if do_all or pseudolandmark:
        transformed_imgs["Pseudolandmark"] = pseudolandmark_transformation(
            image, roi_mask)
    if do_all or edges:
        transformed_imgs["Edges"] = edge_detection_transformation(roi_mask)
    return transformed_imgs
