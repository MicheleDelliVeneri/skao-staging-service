import requests
from fastapi import HTTPException
import os

RUCIO_BASE_URL = os.getenv("RUCIO_BASE_URL", "https://default-rucio-instance")
RUCIO_TOKEN = "your-token"

def get_rucio_headers(rucio_token: str):
    """
    Generate headers with user-provided Rucio token.

    Args:
        rucio_token (str): Rucio token.

    Returns:
        dict: Headers with Rucio token.
    """
    return {"Authorization": f"Bearer {rucio_token}"}


def check_storage_availability(account: str, rse_expression: str, rucio_token: str):
    """
    Verify that data exists at a given scope and name.

    Args:
        scope (str): Scope of the data.
        name (str): Name of the data.
        rucio_token (str): Rucio token.

    Returns:
        dict: Data availability information.

    Raises:
        HTTPException: If the data is not found.
    """
    url = f"{RUCIO_BASE_URL}/accountlimits/global/{account}/{rse_expression}"
    response = requests.get(url, headers=get_rucio_headers(rucio_token))
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Insufficient storage.")
    return response.json()

def verify_data_availability(scope: str, name: str, rucio_token: str):
    """
    Check available storage for the user.

    Args:
        account (str): Account of the user.
        rse_expression (str): RSE expression.
        rucio_token (str): Rucio token.

    Returns:
        dict: Storage availability information.

    Raises:
        HTTPException: If the storage is insufficient.
    """
    url = f"{RUCIO_BASE_URL}/dids/{scope}/{name}"
    response = requests.get(url, headers=get_rucio_headers(rucio_token))
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail=f"Data {scope}:{name} not found.")
    return response.json()

def initiate_transfer(source_rse: str, dest_rse: str, scope: str, name: str, rucio_token: str):
    """
    Initiate data transfer between RSEs.

    Args:
        source_rse (str): Source RSE.
        dest_rse (str): Destination RSE.
        scope (str): Scope of the data.
        name (str): Name of the data.
        rucio_token (str): Rucio token.

    Returns:
        dict: Transfer information.

    Raises:
        HTTPException: If the transfer fails.
    """
    url = f"{RUCIO_BASE_URL}/requests"
    payload = {
        "sources": [{"rse": source_rse}],
        "dest_rse": dest_rse,
        "rule": {"scope": scope, "name": name},
    }
    response = requests.post(url, json=payload, headers=get_rucio_headers(rucio_token))
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Data transfer failed.")
    return response.json()

def monitor_transfer(transfer_id: str, rucio_token: str):
    """
    Initiate data transfer between RSEs.

    Args:
        source_rse (str): Source RSE.
        dest_rse (str): Destination RSE.
        scope (str): Scope of the data.
        name (str): Name of the data.
        rucio_token (str): Rucio token.

    Returns:
        dict: Transfer information.

    Raises:
        HTTPException: If the transfer fails.
    """
    url = f"{RUCIO_BASE_URL}/requests/{transfer_id}/status"
    response = requests.get(url, headers=get_rucio_headers(rucio_token))
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to monitor transfer.")
    return response.json()