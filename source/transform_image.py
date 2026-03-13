import numpy as np

from pathlib import Path
from matplotlib import pyplot as plt
from source.load_image import load_image
from source.transformation.edge_detection import edge_detection
from source.transformation.gaussian_blur import gaussian_blur


def display_images(original_img: np.ndarray,
                   transformed_imgs: dict[str, np.ndarray]) -> None:
    plt.figure(num="Augmented images")

    nb_rows = 1
    nb_cols = 3

    # Places original image in the middle of the first row
    plt.subplot(nb_rows, nb_cols, 1)
    plt.imshow(original_img)
    plt.title("Original")
    plt.axis("off")

    plt.subplot(nb_rows, nb_cols, 2)
    plt.imshow(transformed_imgs["Gaussian blur"], cmap="gray")
    plt.title("Gaussian blur")
    plt.axis("off")

    plt.subplot(nb_rows, nb_cols, 3)
    plt.imshow(transformed_imgs["Edge detection"])
    plt.title("Edge detection")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


def transform_image(image_file_path: Path) -> None:
    image: np.ndarray = load_image(image_file_path)

    transformed_imgs: dict[str, np.ndarray] = {
        "Gaussian blur": gaussian_blur(image),
        "Edge detection": edge_detection(image)
    }

    display_images(image, transformed_imgs)
