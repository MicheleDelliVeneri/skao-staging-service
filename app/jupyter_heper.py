import requests

# Base API URL
JUPYTERHUB_URL = "http://localhost:8080/hub/api"
API_TOKEN = "8179213ad63c46d5b9e4abff384b3e1f"  # Replace with your token
HEADERS = {"Authorization": f"token {API_TOKEN}"}


def get_user_status(username):
    """Get status of a specific user."""
    url = f"{JUPYTERHUB_URL}/user/{username}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get user status: {response.status_code} - {response.text}")

def stop_user_server(username):
    """Stop the user's server."""
    url = f"{JUPYTERHUB_URL}/users/{username}/server"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code in [202, 204]:
        return f"Stopped server for user {username}"
    else:
        raise Exception(f"Failed to stop user server: {response.status_code} - {response.text}")

def start_user_server(username):
    """Start the user's server."""
    url = f"{JUPYTERHUB_URL}/users/{username}/server"
    response = requests.post(url, headers=HEADERS)
    if response.status_code in [201, 202]:
        return f"Started server for user {username}"
    else:
        raise Exception(f"Failed to start user server: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Test API calls
    username = "admin"
    print(f"Fetching status for user {username}...")
    user_status = get_user_status(username)
    print(user_status)

    print(f"Stopping server for user {username}...")
    print(stop_user_server(username))
    print(f"Starting server for user {username}...")
    print(start_user_server(username))
