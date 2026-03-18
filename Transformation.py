import argparse
import sys

from pathlib import Path
from Augmentation import valid_file
from source.transform_image import transform_image
from source.utils.existing_directory import existing_directory


def is_single_file_mode(len_argv: int):
    return len_argv == 2


def is_batch_mode(len_argv: int):
    return len_argv == 5


def argparse_init(len_argv: int) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Transformation.py",
        usage=(
            "python3.13 Transformation.py <image_file>\n"
            "python3.13 Transformation.py -src <directory> -dst <directory>"
        )
    )

    # Single file mode
    if is_single_file_mode(len_argv):
        parser.add_argument(
            "image_file", type=valid_file, help="Input image file"
        )
    # Batch mode
    elif is_batch_mode(len_argv):
        parser.add_argument("-src", help="Source directory",
                            type=existing_directory)
        parser.add_argument("-dest", help="Destination directory",
                            type=existing_directory)

    return parser


def main():
    len_argv = len(sys.argv)
    parser: argparse.ArgumentParser = argparse_init(len_argv)
    args = parser.parse_args()

    # Single image file
    if is_single_file_mode(len_argv):
        image_file_path: Path = Path(args.image_file)
        transform_image(image_file_path)
    # Batch
    elif is_batch_mode(len_argv):
        print(f"Batch mode : src {args.src} | dest {args.dest}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
