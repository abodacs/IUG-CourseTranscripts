import os
from pathlib import Path


def get_empty_directories(path):
    empty_dirs = []
    for dirpath, dirnames, filenames in os.walk(path):
        if not dirnames and not filenames:
            empty_dirs.append(dirpath)
    return empty_dirs


# Example usage
path_to_search = Path(".")
empty_directories = get_empty_directories(path_to_search)
print(empty_directories)
