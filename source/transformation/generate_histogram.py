import io

import cv2
import numpy as np
from matplotlib import pyplot as plt


def generate_histogram(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    img_rgb = image
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)

    channels = {
        'blue': (img_rgb[:, :, 2], 'blue'),
        'blue-yellow': (img_lab[:, :, 2], 'gold'),
        'green': (img_rgb[:, :, 1], 'green'),
        'green-magenta': (img_lab[:, :, 1], 'magenta'),
        'hue': (img_hsv[:, :, 0], 'purple'),
        'lightness': (img_lab[:, :, 0], 'gray'),
        'red': (img_rgb[:, :, 0], 'red'),
        'saturation': (img_hsv[:, :, 1], 'cyan'),
        'value': (img_hsv[:, :, 2], 'orange')
    }

    fig, ax = plt.subplots(figsize=(8, 5))

    total_pixels = cv2.countNonZero(mask) if mask is not None else img_rgb.shape[0] * img_rgb.shape[1]

    for name, (chan_data, color) in channels.items():
        hist = cv2.calcHist([chan_data], [0], mask, [256], [0, 256])

        if total_pixels > 0:
            hist_percent = (hist / total_pixels) * 100
        else:
            hist_percent = hist

        ax.plot(hist_percent, color=color, label=name, linewidth=1.2)

    ax.set_title("Color histogram", fontsize=12)
    ax.set_xlabel("Pixel intensity", fontsize=10)
    ax.set_ylabel("Proportion of pixels (%)", fontsize=10)

    ax.legend(title="color Channel", loc="center left", bbox_to_anchor=(1.02, 0.5), frameon=False)
    ax.grid(True, color='white', linewidth=1.5)
    ax.set_xlim([0, 256])

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', dpi=100)
    buf.seek(0)

    hist_img = cv2.imdecode(np.frombuffer(buf.getvalue(), dtype=np.uint8), cv2.IMREAD_COLOR)
    hist_img = cv2.cvtColor(hist_img, cv2.COLOR_BGR2RGB)

    plt.close(fig)

    return hist_img