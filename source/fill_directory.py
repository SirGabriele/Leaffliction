from pathlib import Path


def fill_directory(directory: Path, max_count: int, filter_functions: list[callable]):
    images: list[Path] = [
        f for f in directory.iterdir()
        if f.suffix.lower() == ".jpg"
    ]

    # For directory with max_count images, no need to fill it
    if len(images) == max_count:
        return

    len_filter_functions = len(filter_functions)
    for i, image in enumerate(images):
        # Must iterate through images and duplicate them
        filter_functions[i % len_filter_functions](image)
        pass
    # print(images)
