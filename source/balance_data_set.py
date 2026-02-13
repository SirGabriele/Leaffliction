from source.fill_directory import fill_directory
from source.filters.blur import blur
from source.filters.contrast import contrast
from source.filters.flip import flip
from source.filters.illuminate import illuminate
from source.filters.rotate import rotate
from source.filters.scale import scale
from pathlib import Path


def balance_data_set(root_directory: Path, counts: list[int]):
    max_count = max(counts)
    filter_functions: list[callable] = [
        blur,
        contrast,
        flip,
        illuminate,
        rotate,
        scale,
    ]

    for subdir in root_directory.iterdir():
        if subdir.is_dir():
            fill_directory(subdir, max_count, filter_functions)
