import argparse
import os

from pathlib import Path
from source.balance_data_set import balance_data_set
from source.count_images import count_images
from source.plot_charts import plot_charts


def existing_folder(path: str) -> str:
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Directory '{path}' does not exist")
    return path


def argparse_init() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Run Distribution program with an input folder',
        usage="python3.10 Distribution.py <folder>"
    )
    parser.add_argument(
        'folder',
        type=existing_folder,
        help='Path to the root directory'
    )
    return parser


def main():
    parser: argparse.ArgumentParser = argparse_init()
    root_directory_name: str = parser.parse_args().folder
    root_directory: Path = Path(root_directory_name)

    labels, counts = count_images(root_directory)
    if not labels:
        print("No subfolder containing JPG images found.")
        return

    # plot_charts(root_name, labels, counts)
    balance_data_set(root_directory, counts)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
