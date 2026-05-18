import argparse
import json

import cv2
import tensorflow as tf
import numpy as np

from matplotlib import pyplot as plt
from source.load_image import load_image
from source.transform_image import transform_image
from source.utils.valid_file import valid_file


def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run training',
        usage="./venv/bin/python3.10 predict.py <image file>"
    )
    parser.add_argument(
        'image_file',
        type=valid_file,
        help='Path to the image file'
    )
    return parser


def main():
    args = argparse_init().parse_args()
    img = load_image(args.image_file)

    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.axis('off')

    transformed_dict = transform_image(img, background_removal=True)

    key_roi = "Background removal"
    if key_roi not in transformed_dict:
        print(f"Error : transformation '{key_roi}' failed.")
        return

    img_transformed_rgb = transformed_dict[key_roi]
    plt.subplot(1, 2, 2)
    plt.imshow(img_transformed_rgb)
    plt.axis('off')

    model = tf.keras.models.load_model("leaf_model.keras")
    img_ready = cv2.resize(img_transformed_rgb, (128, 128))
    img_normalized = img_ready.astype("float32")
    img_final = np.expand_dims(img_normalized, axis=0)
    predictions = model.predict(img_final, verbose=0)
    class_idx = np.argmax(predictions[0])

    try:
        with open("class_names.json", "r") as f:
            class_names = json.load(f)
    except FileNotFoundError:
        print("Error : file 'class_names.json' not found.")
        return

    class_name = class_names[class_idx]

    plt.figtext(0.5,
                0.15,
                f"Class predicted: {class_name}",
                horizontalalignment='center',
                fontsize=20)

    plt.show()
    exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(err)
