import argparse

from pathlib import Path
from source.augment_image import augment_image
from source.utils.valid_file import valid_file


def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run Augmentation program with an input JPG file',
        usage="python3.10 Augmentation.py <image_file>"
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
