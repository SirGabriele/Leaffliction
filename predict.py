import argparse
import json

import cv2
import tensorflow as tf
import numpy as np

from matplotlib import pyplot as plt
from source.load_image import load_image
from source.transform_image import transform_image


from source.utils.existing_directory import existing_directory

def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run training',
        usage="python3.13 train.py <directory>"
    )
    parser.add_argument(
        'directory',
        help='Path to the directory file'
    )
    return parser


def main():
    args = argparse_init().parse_args()
    img = load_image(args.directory)

    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.title("Original")
    plt.axis('off')

    transformed_dict = transform_image(img, background_removal=True)

    key_roi = "Background removal"
    if key_roi not in transformed_dict:
        print(f"Erreur : La transformation '{key_roi}' a échoué.")
        return

    img_transformed_rgb = transformed_dict[key_roi]
    plt.subplot(1, 2, 2)
    plt.imshow(img_transformed_rgb)
    plt.axis('off')

    model = tf.keras.models.load_model("leaf_model.keras")
    img_ready = cv2.resize(img_transformed_rgb, (128, 128))
    img_normalized = img_ready.astype("float32")
    img_final = np.expand_dims(img_normalized, axis=0)
    predictions = model.predict(img_final, verbose=0)  # verbose=0 pour pas de logs inutiles

    # 4. INTERPRÉTER LE RÉSULTAT
    # predictions est un tableau de probabilités, on prend l'indice le plus élevé
    class_idx = np.argmax(predictions[0])

    # --- LECTURE DU JSON ---
    try:
        with open("class_names.json", "r") as f:
            class_names = json.load(f)
    except FileNotFoundError:
        print("Erreur : Le fichier 'class_names.json' est introuvable.")
        print("Assure-toi de l'avoir généré lors de l'entraînement.")
        return

    # On récupère le nom de la maladie
    resultat = class_names[class_idx]

    # Bonus : On calcule le pourcentage de certitude de l'IA
    confiance = 100 * np.max(predictions[0])

    print(f"Maladie détectée : {resultat} (Confiance : {confiance:.2f}%)")

    plt.show()

    plt.show()
    exit(0)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as err:
        print(err)