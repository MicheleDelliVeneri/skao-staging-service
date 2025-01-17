import os
from shutil import copy

# Staging method: Copy
def method_1(local_path, relative_path):
    copy(local_path, relative_path)

# Staging method: Symlink
def method_2(local_path, relative_path):
    os.symlink(local_path, relative_path)

# Add more methods as needed

# Dictionary of available methods
AVAILABLE_METHODS = {
    "method_1": method_1,
    "method_2": method_2,
}