import argparse
import os


def existing_directory(path: str) -> str:
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"Directory '{path}' does not exist")
    return path
