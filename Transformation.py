import argparse
import os
import sys
import warnings
import cv2
import numpy as np

from tqdm import tqdm
from pathlib import Path
from source.load_image import load_image
from source.transform_image import transform_image, display_images
from source.utils.valid_file import valid_file
from source.utils.existing_directory import existing_directory
from concurrent.futures import ProcessPoolExecutor, as_completed

warnings.simplefilter(action='ignore', category=FutureWarning)

def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Transformation.py",
        epilog="Usage examples :\n"
               "  python Transformation.py image.jpg\n"
               "  python Transformation.py -src input_dir -dst output_dir --mask -b",
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

    parser.add_argument("-m", "--mask", action="store_true", help="Apply mask to the image transformation")
    parser.add_argument("-s", "--saturation", action="store_true", help="Apply saturation to the image transformation")
    parser.add_argument('-r', '--roi', action="store_true", help="Apply region of interest to the image transformation")
    parser.add_argument('-a', '--analysis', action="store_true", help="Apply analysis to the image transformation")
    parser.add_argument('-p', '--pseudolandmark', action="store_true", help="Apply pseudolandmark to the image transformation")
    parser.add_argument('-e', '--edges', action="store_true", help="Apply edges detection to the image transformation")
    return parser

def validate_arguments_or_fail(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    if args.image_file and (args.source or args.destination):
        parser.error("You cannot provide both an image file and source/destination directories.")
    if (not args.destination and args.source) or (args.destination and not args.source):
        parser.error("Both source and destination directories must be provided together.")
    if not args.image_file and not (args.source and args.destination):
        parser.error("You must provide either a single image file or both source and destination directories.")


def process_single_image_worker(rel_path: Path, source: Path, destination: Path, args: argparse.Namespace) -> tuple[
    bool, str]:
    try:
        image_file_path: Path = source / rel_path
        image: np.ndarray = load_image(image_file_path)

        transformed_images = transform_image(image, args)
        dest_sub_dir = destination / rel_path.parent
        dest_sub_dir.mkdir(parents=True, exist_ok=True)

        for title, img in transformed_images.items():
            output_file_name = f"{rel_path.stem}_{title.replace(' ', '_')}.png"
            output_file_path = dest_sub_dir / output_file_name

            if len(img.shape) == 3:  # Si c'est une image couleur
                img_to_save = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            else:
                img_to_save = img

            cv2.imwrite(str(output_file_path), img_to_save)

        return True, str(rel_path)
    except Exception as e:
        return False, f"Error with {rel_path}: {str(e)}"


def handle_single_file_mode(args: argparse.Namespace) -> None:
    print(f"Single file mode : src {args.image_file}")
    image_file_path: Path = Path(args.image_file)
    image: np.ndarray = load_image(image_file_path)
    transformed_images = transform_image(image, args)
    display_images(image, transformed_images)

def handle_batch_mode(args: argparse.Namespace) -> None:
    print(f"Batch mode :\n\t- Source = {args.source}\n\t- Destination = {args.destination}")
    source_path = Path(args.source)
    dest_path = Path(args.destination)
    valid_extensions = {'.jpg', '.jpeg', '.png'}
    if not os.path.isdir(args.destination):
        Path(args.destination).mkdir(parents=True, exist_ok=True)
    images_to_process = [
        p for p in source_path.rglob('*')
        if p.is_file() and p.suffix.lower() in valid_extensions
    ]
    print(f"\t- Found {len(images_to_process)} image(s) to process.")
    if not images_to_process:
        print("No image files found in the source directory.", file=sys.stderr)
        sys.exit(1)
    with ProcessPoolExecutor() as executor:
        futures = []
        for img_path in images_to_process:
            rel_path = img_path.relative_to(source_path)
            futures.append(
                executor.submit(process_single_image_worker, rel_path, source_path, dest_path, args)
            )

        for future in tqdm(as_completed(futures), total=len(images_to_process), desc="Processing images", unit="img"):
            success, result_message = future.result()
            if not success:
                tqdm.write(result_message)

def main():
    parser: argparse.ArgumentParser = argparse_init()
    args = parser.parse_args()
    validate_arguments_or_fail(args, parser)

    if args.image_file:
        handle_single_file_mode(args)
    else:
        handle_batch_mode(args)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
