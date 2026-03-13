import argparse
from pathlib import Path

from Augmentation import valid_file
from source.transform_image import transform_image
from source.utils.existing_directory import existing_directory


def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Transformation.py",
        usage=(
            "python3.13 Transformation.py <image_file>\n"
            "python3.13 Transformation.py -src <directory> -dst <directory>"
        )
    )

    # Single file mode
    parser.add_argument(
        "image_file",
        nargs="?",
        type=valid_file,
        help="Input image file"
    )

    # Batch mode
    parser.add_argument(
        "-src", help="Source directory", type=existing_directory
    )
    parser.add_argument(
        "-dest", help="Destination directory", type=existing_directory
    )

    return parser


def main():
    parser: argparse.ArgumentParser = argparse_init()
    args = parser.parse_args()

    # Single image file
    if args.image_file and not args.src:
        image_file_path: Path = Path(parser.parse_args().image_file)
        transform_image(image_file_path)
    # Batch
    elif args.src and args.dest:
        print(f"Batch mode : src {args.src} | dest {args.dest}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
