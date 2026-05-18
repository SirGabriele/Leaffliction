# Leaffliction

## Getting started

### Requirements

- python3.10
- make
- pip

# Distribution

The distribution program reads the specified directory and its direct 
subdirectories.

```text
$ find images/ -maxdepth 2 -type d
images/
images/Grape_Esca
images/Apple_Black_rot
images/Apple_rust
images/Grape_healthy
images/Grape_spot
images/Apple_healthy
images/Apple_scab
images/Grape_Black_rot
```

It will display one pie chart and one bar chart that show the amount of 
files per subdirectory.

```python3.10
venv/bin/python3.10 Distribution.py <data_set_directory>
```

![Distribution charts](resource/distribution_charts.png)

# Augmentation

We notice that the data set is not balanced. In order to balance it, we 
will create variations of the existing images by applying different filters 
on them.

We have implemented 6 different kinds of filters :
- Blur : blurs the image
- Flip : flips the image
- Illuminate : increases the alpha of the image
- Project : applies a distortion to the image
- Rotate : rotates the image
- Scale : zooms in/out of the image

All filters have properties that are configurable in `config.py`. If 
`DISPLAY_AUGMENTED_IMAGES` is set to true, the program will open a window 
to display all augmented images.

![Augmented images](resource/augmented_images.png)

# Transformation

This part of the program aims to extract features and highlight specific regions of interest (ROI) on the leaves, such as diseased areas, to better understand the data.

We have implemented 6 different transformations that can be applied to the images:
- **Mask (`-m`, `--mask`)** : Generates a binary region of interest (ROI) mask.
- **Saturation (`-s`, `--saturation`)** : Applies a saturation transformation to the image.
- **ROI (`-r`, `--roi`)** : Highlights the diseased areas based on the mask.
- **Analysis (`-a`, `--analysis`)** : Analyzes the region of interest.
- **Pseudolandmark (`-p`, `--pseudolandmark`)** : Extracts and displays pseudolandmarks on the leaf.
- **Edges (`-e`, `--edges`)** : Detects the edges of the region of interest.

> [!NOTE]
> If no specific filter flag is provided, **all** transformations are applied by default.

The program operates in two distinct modes depending on the provided arguments:

### 1. Single File Mode
Processes a single image and opens a `matplotlib` window to display the original image alongside the requested transformations. 

```bash
$ ./venv/bin/python3.10 Transformation.py <image_file>
```

![Transformed images](resource/transformed_images.png)

### 2. Batch Mode
Processes an entire directory (and its subdirectories) using multiprocessing to speed up the execution. It applies the selected transformations to all valid images and saves the results in a specified destination folder. 

```bash
$ ./venv/bin/python3.10 Transformation.py -src <source_directory> -dst <destination_directory> [options]
```

**Example:** Applying only the Mask and Edges transformations to a dataset:
```bash
$ ./venv/bin/python3.10 Transformation.py -src images/ -dst transformed_data/ --mask --edges
```

# Classification

## Training

The training program takes a directory of labelled images (one subdirectory per class) and runs the following pipeline:

1. **Balancing** — copies all images into a `balanced_images/` directory and augments under-represented classes until each reaches a target of 2000 images.
2. **Transformation** — applies background removal to every image and saves the results in a `transformation_images/` directory.
3. **Training** — trains a CNN on the transformed images for 30 epochs with an 80/20 train/validation split.
4. **Saving** — writes the trained model to `leaf_model.keras`, the class labels to `class_names.json`, and packages everything into `training_results.zip`.

Training parameters are configurable in `config.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `IMAGE_SIZE` | `(128, 128)` | Input image resolution |
| `BATCH_SIZE` | `32` | Mini-batch size |
| `CONV_FILTERS` | `(32, 64, 128)` | Filters per Conv2D layer |
| `DENSE_UNITS` | `128` | Units in the fully-connected layer |

```bash
$ venv/bin/python3.10 train.py <data_set_directory>
```

### Model architecture

```
Input (128×128 RGB)
└── Rescaling (÷255)
└── Conv2D(32, 3×3, relu) → MaxPooling2D(2×2)
└── Conv2D(64, 3×3, relu) → MaxPooling2D(2×2)
└── Conv2D(128, 3×3, relu) → MaxPooling2D(2×2)
└── Flatten
└── Dense(128, relu)
└── Dropout(0.5)
└── Dense(N classes, softmax)
```

Optimizer: **Adam** | Loss: **sparse categorical crossentropy** | Epochs: **30**

The validation set represents 20% of the data and achieves above 90% accuracy.

## Prediction

The prediction program loads the saved model and classifies a single image. It displays the original image alongside the background-removed version, and prints the predicted disease class below both images.

```bash
$ venv/bin/python3.10 predict.py <image_file>
```

![Prediction output](resource/prediction.png)