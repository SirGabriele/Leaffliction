from pathlib import Path


def count_images(root_directory: Path) -> tuple[list[str], list[int]]:
    class_names: list[str] = []
    counts: list[int] = []

    for subdir in root_directory.iterdir():
        if subdir.is_dir():
            images: list[Path] = [
                f for f in subdir.iterdir()
                if f.suffix.lower() == ".jpg"
            ]

            if images:
                class_names.append(subdir.name)
                counts.append(len(images))

    return class_names, counts
