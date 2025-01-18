import os
from shutil import copy, copytree
import logging
from fastapi.responses import FileResponse
from app.jupyter_helper import get_user_status, start_user_server
import requests

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
# --------------------------- COPY       --------------------------------------------
def local_copy(local_path, relative_path):
    """
    Copies a file or directory from the local storage to the user area.

    Parameters
    ----------
    local_path : str
        Path to the file or directory on the local storage.
    relative_path : str
        Path to the file or directory relative to the user area.

    Raises
    ------
    ValueError
        If the path provided is invalid.
    Exception
        If any other error occurs during the copy operation.
    """
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
# --------------------------- SYMLINK COPY --------------------------------------------
def local_symlink(local_path, relative_path):
    """
    Creates a symlink from the local storage to the user area.

    Parameters
    ----------
    local_path : str
        Path to the file or directory on the local storage.
    relative_path : str
        Path to the file or directory relative to the user area.

    Raises
    ------
    ValueError
        If the path provided is invalid.
    Exception
        If any other error occurs during the symlink operation.
    """
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

# Staging method: Direct Download
# --------------------------- DIRECT DOWNLOAD --------------------------------------------
def direct_download(local_path):
    """
    Serves a file from the local storage using a direct download.

    Parameters
    ----------
    local_path : str
        Path to the file on the local storage.

    Returns
    -------
    FileResponse
        A FileResponse object containing the file contents.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the provided path.
    Exception
        If any other error occurs during the direct download operation.
    """
    try:
        logger.info(f"Starting direct_download for path {local_path}")

        if not os.path.exists(local_path):
            logger.error(f"File not found at path: {local_path}")
            raise FileNotFoundError(f"File not found at path: {local_path}")

        # Return a FileResponse for FastAPI to serve the file
        logger.info(f"Serving file from path: {local_path}")
        return FileResponse(local_path, media_type='application/octet-stream', filename=os.path.basename(local_path))

    except Exception as e:
        logger.error(f"Error during direct_download: {e}")
        raise


# Staging method: Jupyter Copy
# --------------------------- JUPYTER COPY --------------------------------------------
def jupyter_copy(local_path, relative_path, username, token):
    """
    Copies a file from the local storage to the user's Jupyter server.

    Parameters
    ----------
    local_path : str
        Path to the file on the local storage.
    relative_path : str
        Path to the file relative to the user area.
    username : str
        Username of the user to copy the file for.
    token : str
        Token to use for authentication with the Jupyter server.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the provided path.
    Exception
        If any other error occurs during the copy operation.
    """
    try:
        logger.info(f"Starting jupyter_copy for user {username}")

        # Ensure the server is running
        hub_url = os.getenv("JUPYTERHUB_URL", "http://localhost:8080")
        user_status = get_user_status(username)

        if "servers" not in user_status or not user_status["servers"]:
            logger.info(f"Server not running for user {username}. Starting server...")
            start_user_server(username, hub_url)

        # Refresh user status
        user_status = get_user_status(username)
        server_info = user_status.get("servers", {}).get("", None)
        if not server_info or not server_info.get("ready", False):
            raise Exception(f"Failed to start or verify readiness of server for user {username}.")

        # Check if the file exists on the Jupyter server
        jupyter_path = relative_path
        url = f"{hub_url}/hub/api/users/{username}/servers/{jupyter_path}/api/contents/{jupyter_path}"
        headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            logger.info(f"File already exists at {jupyter_path} for user {username}")
            return

        # File does not exist; proceed with the copy
        with open(local_path, 'rb') as file:
            data = {
                "content": file.read().decode('utf-8'),
                "format": "text",
                "type": "file"
            }
            response = requests.put(url, headers=headers, json=data)

            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to copy file: {response.status_code} - {response.text}")

        logger.info(f"Successfully copied file to {jupyter_path} for user {username}")

    except Exception as e:
        logger.error(f"Error during jupyter_copy for user {username}: {e}")
        raise

# Add jupyter_copy to AVAILABLE_METHODS
AVAILABLE_METHODS: dict[str, callable] = {
    "local_copy": local_copy,
    "local_symlink": local_symlink,
    "jupyter_copy": jupyter_copy,
    "direct_download": direct_download,
}