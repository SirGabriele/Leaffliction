import argparse
import sys
from pathlib import Path

import numpy as np

from source.load_image import load_image
from source.transform_image import transform_image, display_images
from source.utils.valid_file import valid_file
from source.utils.existing_directory import existing_directory


def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Transformation.py",
        epilog="Usage exemples :\n"
               "  python Transformation.py image.jpg\n"
               "  python Transformation.py -src input_dir -dst output_dir -mask",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Single file mode
    parser.add_argument(
        "image_file",
        nargs="?",
        type=valid_file,
        help="Input image file"
    )
    parser.add_argument("-src", "--source",
                        help="Source directory",
                        type=existing_directory)
    parser.add_argument("-dst", "--destination",
                        help="Destination directory")

    parser.add_argument("-b", "--blur", action="store_true", help="Apply blur to the image transformation")
    parser.add_argument("-m", "--mask", action="store_true", help="Apply mask to the image transformation")
    parser.add_argument('-r', '--roi', action="store_true", help="Apply region of interest to the image transformation")
    parser.add_argument('-a', '--analysis', action="store_true", help="Apply analysis to the image transformation")
    parser.add_argument('-p', '--pseudolandmark', action="store_true", help="Apply pseudolandmark to the image transformation")
    parser.add_argument('-c', '--color-histogram', action="store_true", help="Apply color histogram to the image transformation")
    return parser

def validate_arguments_or_raise(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if args.image_file and (args.source or args.destination):
        parser.error("You cannot provide both an image file and source/destination directories.")
    if (not args.destination and args.source) or (args.destination and not args.source):
        parser.error("Both source and destination directories must be provided together.")
    if not args.image_file and not (args.source and args.destination):
        parser.error("You must provide either a single image file or both source and destination directories.")

def handle_single_file_mode(args: argparse.Namespace) -> None:
    print(f"Single file mode : src {args.image_file}")
    image_file_path: Path = Path(args.image_file)
    image: np.ndarray = load_image(image_file_path)
    transformed_images = transform_image(image, args)
    display_images(image, transformed_images)

def main():
    parser: argparse.ArgumentParser = argparse_init()
    args = parser.parse_args()
    validate_arguments_or_raise(args, parser)

    if args.image_file:
        handle_single_file_mode(args)
    else:
        print(f"Batch mode : src {args.source} | dest {args.destination}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
