# Leaffliction

## Getting started

### Requirements

- python3.13.5
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

```python3.13
venv/bin/python3.13 Distribution.py <data_set_directory>
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

![Augmented images](resource/augmentation_window.png)
