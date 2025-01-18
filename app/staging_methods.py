import os
from shutil import copy, copytree
import logging

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO").upper()
# Set up logging
logging.basicConfig(
    level=getattr(logging, LOGGING_LEVEL, logging.INFO),  # Set logging level to DEBUG for detailed logs
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(), # Log to console
        logging.FileHandler("staging_service.log")
    ]
)
logger = logging.getLogger(__name__)

# Staging method: Copy
def local_copy(local_path, relative_path):
    try:
        logger.info(f"Starting local_copy from {local_path} to {relative_path}")
        if os.path.isdir(local_path):
            # Copy entire directory
            copytree(local_path, relative_path, dirs_exist_ok=True)
            logger.info(f"Copied directory from {local_path} to {relative_path}")
        elif os.path.isfile(local_path):
            # Copy single file
            copy(local_path, relative_path)
            logger.info(f"Copied file from {local_path} to {relative_path}")
        else:
            raise ValueError(f"Invalid path: {local_path}")
    except Exception as e:
        logger.error(f"Error during local_copy from {local_path} to {relative_path}: {e}")
        raise

# Staging method: Symlink
def local_symlink(local_path, relative_path):
    try:
        logger.info(f"Starting local_symlink from {local_path} to {relative_path}")
        if os.path.isdir(local_path):
            # Create a symlink for the directory
            os.symlink(local_path, relative_path, target_is_directory=True)
            logger.info(f"Created directory symlink from {local_path} to {relative_path}")
        elif os.path.isfile(local_path):
            # Create a symlink for the file
            os.symlink(local_path, relative_path)
            logger.info(f"Created file symlink from {local_path} to {relative_path}")
        else:
            raise ValueError(f"Invalid path: {local_path}")
    except Exception as e:
        logger.error(f"Error during local_symlink from {local_path} to {relative_path}: {e}")
        raise
# Add more methods as needed

# Dictionary of available methods
AVAILABLE_METHODS: dict[str, callable] = {
    "local_copy": local_copy,
    "local_symlink": local_symlink,
}