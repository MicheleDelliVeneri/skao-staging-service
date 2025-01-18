import os
from shutil import copy, copytree

# Staging method: Copy
def local_copy(local_path, relative_path):
    if os.path.isdir(local_path):
        # Copy entire directory
        copytree(local_path, relative_path, dirs_exist_ok=True)
    elif os.path.isfile(local_path):
        # Copy single file
        copy(local_path, relative_path)
    else:
        raise ValueError(f"Invalid path: {local_path}")

# Staging method: Symlink
def local_symlink(local_path, relative_path):
    if os.path.isdir(local_path):
        # Create a symlink for the directory
        os.symlink(local_path, relative_path, target_is_directory=True)
    elif os.path.isfile(local_path):
        # Create a symlink for the file
        os.symlink(local_path, relative_path)
    else:
        raise ValueError(f"Invalid path: {local_path}")

# Add more methods as needed

# Dictionary of available methods
AVAILABLE_METHODS: dict[str, callable] = {
    "local_copy": local_copy,
    "local_symlink": local_symlink,
}