import argparse

from pathlib import Path
from source.count_images import count_images
from source.plot_charts import plot_charts
from source.utils.existing_directory import existing_directory


def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run Distribution program with an input directory',
        usage="python3.13 Distribution.py <directory>"
    )
    parser.add_argument(
        'directory',
        type=existing_directory,
        help='Path to the root directory'
    )
    return parser


def main():
    parser: argparse.ArgumentParser = argparse_init()
    root_directory_name: str = parser.parse_args().directory
    root_directory: Path = Path(root_directory_name)

    count_images_dir = count_images(root_directory)
    if not count_images_dir :
        print("No subdirectory containing JPG images_dir found.")
        return

    plot_charts(root_directory_name, list(count_images_dir.keys()), list(count_images_dir.values()))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
