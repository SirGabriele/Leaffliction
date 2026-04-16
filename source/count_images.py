from pathlib import Path


def count_images(root_directory: Path) -> dict[str, int]:
    result = dict()

    for subdir in root_directory.iterdir():
        if subdir.is_dir():
            images: list[Path] = [
                f for f in subdir.iterdir()
                if f.suffix.lower() == ".jpg"
            ]

            if images:
                result[subdir.name] = len(images)

    return result
