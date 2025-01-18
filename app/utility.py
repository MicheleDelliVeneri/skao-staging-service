import os
import pwd
import grp
from fastapi import HTTPException
import subprocess
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




def set_read_only(path, username):
    """Set read-only permissions and ownership for a specific user."""
    try:
        # Get UID and GID for the user
        user_info = pwd.getpwnam(username)
        uid = user_info.pw_uid
        gid = user_info.pw_gid

        if os.path.isfile(path):
            os.chmod(path, 0o400)  # Read-only for owner
            os.chown(path, uid, gid)  # Change ownership to the user
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.chmod(file_path, 0o400)  # Read-only for owner
                    os.chown(file_path, uid, gid)  # Change ownership to the user
                for directory in dirs:
                    dir_path = os.path.join(root, directory)
                    os.chmod(dir_path, 0o500)  # Read-only and traversable for owner
                    os.chown(dir_path, uid, gid)  # Change ownership to the user
            os.chmod(path, 0o500)  # Read-only and traversable for the root directory
            os.chown(path, uid, gid)  # Change ownership to the root directory
    except KeyError:
        raise HTTPException(status_code=400, detail=f"User {username} does not exist.")

def ensure_user_exists(username: str):
    """Ensure the user exists on the system. Skip creation in test environments."""
    if os.getenv("TEST_ENV", "false") == "true":
        logger.debug(f"Skipping user creation for testing: {username}")
        return

    try:
        result = subprocess.run(
            ["id", username],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if result.returncode != 0:
            logger.info(f"User {username} does not exist. Creating user.")
            subprocess.run(["useradd", "-m", username], check=True)
            logger.info(f"User {username} created successfully.")
        else:
            logger.debug(f"User {username} already exists.")
    except Exception as e:
        logger.exception(f"Failed to ensure user exists: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ensure user exists: {str(e)}"
        )
