import argparse
import os

from pathlib import Path
from source.augment_image import augment_image


def valid_file(path: str) -> str:
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File '{path}' does not exist")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Read permission is not granted for '{path}'")
    return path


def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run Augmentation program with an input JPG file',
        usage="python3.13 Augmentation.py <image_file>"
    )
    parser.add_argument(
        'image_file',
        type=valid_file,
        help='Path to the image file'
    )
    return parser


def main():
    parser: argparse.ArgumentParser = argparse_init()
    image_file_name: str = parser.parse_args().image_file
    image_file_path: Path = Path(image_file_name)

    augment_image(image_file_path)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
