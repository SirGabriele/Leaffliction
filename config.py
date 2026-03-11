AUGMENTED_DIRECTORY = "augmented_directory"

# Filters config

DISPLAY_AUGMENTED_IMAGES = True

BLUR_KERNEL_SIZE = 5

# 0 for horizontal rotation.
# > 0 for vertical rotation.
# < 0 for both.
FLIP_ROTATION_AXIS = 1

SCALE_FACTOR = 1.5

ROTATION_ANGLE = 45

ILLUMINATE_ALPHA = 1.5
ILLUMINATE_BETA = 0

# (x, y) projection factors for each corner of the image.
# An x value close to 0 will bring the point to the left.
# An x value close to 1 will bring the point to the right.
# A y value close to 0 will bring the point to the top.
# A y value close to 1 will bring the point to the bottom.
#    (0, 0)        (1, 0)
#       ●────────────●
#       │            │
#       │            │
#       │            │
#       │            │
#       ●────────────●
#    (0, 1)        (1, 1)
PROJECTION_TOP_LEFT_FACTORS = (0.05, 0.3)
PROJECTION_TOP_RIGHT_FACTORS = (0.8, 0.1)
PROJECTION_BOTTOM_RIGHT_FACTORS = (0.8, 0.6)
PROJECTION_BOTTOM_LEFT_FACTORS = (0.4, 0.9)
