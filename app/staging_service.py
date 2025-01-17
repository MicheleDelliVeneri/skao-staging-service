from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, ConfigDict
import os
from typing import List, Literal
from app.staging_methods import AVAILABLE_METHODS
import json
# FastAPI application
app = FastAPI(title="Data Staging Service")

# Configuration placeholder (overrideable via Helm values)
SITE_CONFIG = {
    "base_user_area_path": "/tmp/user_areas/",
    "allowed_methods": list(AVAILABLE_METHODS.keys()),  # Load methods dynamically
    "storage_paths": {
        "site_a": "/tmp/storage_a/",
        "site_b": "/tmp/storage_b/",
    },
}

# Request model
class StagingRequest(BaseModel):
    data: List[dict]
    method: Literal["method_1", "method_2"]
    username: str

# Dependency for configuration
def get_config():
    return SITE_CONFIG

# Utility function: validate paths
def validate_and_prepare_paths(data, site_config, username):
    user_area = os.path.join(site_config["base_user_area_path"], username)
    os.makedirs(user_area, exist_ok=True)
    staging_paths = []
    for item in data:
        local_path = item["local_path_on_storage"]
        relative_path = os.path.join(user_area, item["relative_path"])

        if not os.path.exists(local_path):
            raise HTTPException(status_code=400, detail=f"Path {local_path} does not exist.")
        os.makedirs(os.path.dirname(relative_path), exist_ok=True)
        staging_paths.append((local_path, relative_path))

    return staging_paths

# Endpoint for staging data
@app.post("/stage-data/")
async def stage_data(request: StagingRequest, site_config: dict = Depends(get_config)):
    if request.method not in site_config["allowed_methods"]:
        raise HTTPException(status_code=400, detail="Invalid staging method.")

    try:
        staging_paths = validate_and_prepare_paths(request.data, site_config, request.username)
    except HTTPException as e:
        raise e

    for local_path, relative_path in staging_paths:
        try:
            # Dynamically call the method based on the request
            method_func = AVAILABLE_METHODS[request.method]
            method_func(local_path, relative_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing path {local_path}: {str(e)}")

    return {"status": "success", "message": "Data staged successfully"}

