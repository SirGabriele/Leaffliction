from config import AUGMENTED_DIRECTORY
from pathlib import Path


def create_augmented_directory(image_file_path: Path) -> Path:
    augmented_directory_path = (
            Path(AUGMENTED_DIRECTORY)
            / image_file_path.parent.name
    )
    augmented_directory_path.mkdir(parents=True, exist_ok=True)
    return augmented_directory_path
