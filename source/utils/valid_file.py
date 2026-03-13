import argparse
import os


def valid_file(path: str) -> str:
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"File '{path}' does not exist")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"Read permission is not granted for '{path}'")
    return path
