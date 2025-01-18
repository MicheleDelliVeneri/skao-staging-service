import requests
import time
import json
import logging
import os
from fastapi import HTTPException

JUPYTERHUB_URL = "http://localhost:8080/hub/api"
API_TOKEN = "8179213ad63c46d5b9e4abff384b3e1f"
HEADERS = {"Authorization": f"token {API_TOKEN}"}
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

def event_stream(session, url):
    """Generator yielding events from a JSON event stream."""
    r = session.get(url, stream=True)
    r.raise_for_status()
    for line in r.iter_lines():
        line = line.decode('utf8', 'replace')
        if line.startswith('data:'):
            yield json.loads(line.split(':', 1)[1])


def get_user_status(user_name):
    """Get detailed user status."""
    try:
        url = f"{JUPYTERHUB_URL}/hub/api/users/{user_name}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.exception(f"Failed to fetch user status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch user status: {e}")


def start_user_server(user_name, server_name=""):
    """Start a JupyterHub server and wait for it to be ready."""
    user_url = f"{JUPYTERHUB_URL}/users/{user_name}"
    session = requests.Session()

    # Check user status
    user_model = get_user_status(user_name)
    if server_name not in user_model.get('servers', {}):
        # Server not active, request launch
        response = session.post(f"{user_url}/servers/{server_name}", headers=HEADERS)
        response.raise_for_status()

        if response.status_code == 202:
            # Wait for the server to be ready
            progress_url = f"{user_model['servers'][server_name]['progress_url']}"
            for event in event_stream(session, f"{JUPYTERHUB_URL}{progress_url}"):
                print(f"Progress {event['progress']}%: {event['message']}")
                if event.get("ready"):
                    return event["url"]

    # Server is already running or just launched
    server = user_model["servers"][server_name]
    return server["url"]


def stop_user_server(user_name, server_name=""):
    """Stop a server and wait for it to complete."""
    user_url = f"{JUPYTERHUB_URL}/users/{user_name}"
    server_url = f"{user_url}/servers/{server_name}"
    session = requests.Session()

    response = session.delete(server_url, headers=HEADERS)
    if response.status_code == 404:
        print(f"Server {user_name}/{server_name} already stopped.")
        return

    response.raise_for_status()

    # Wait for the server to be stopped
    while True:
        user_model = get_user_status(user_name)
        if server_name not in user_model.get("servers", {}):
            print(f"Server {user_name}/{server_name} stopped.")
            break

        time.sleep(1)