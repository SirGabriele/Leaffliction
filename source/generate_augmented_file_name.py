from pathlib import Path


def generate_augmented_file_name(image_file_path: Path, filter_suffix: str) -> Path:
    return Path(f"{image_file_path.stem}_{filter_suffix}{image_file_path.suffix}")
