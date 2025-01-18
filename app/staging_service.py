from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, Field, ConfigDict
import os
from typing import List
import json
from app.staging_methods import AVAILABLE_METHODS
from app.utility import set_read_only, ensure_user_exists
import logging
# FastAPI application
app = FastAPI(title="SKAO Data Staging Service")
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

# --------------------------- REQUEST AND RESPONSE MODELS --------------------------------------------
class DataItem(BaseModel):
    local_path_on_storage: str = Field(
        ...,
        description="Local path on storage where the file currently resides."
    )
    relative_path: str = Field(
        ...,
        description="Relative path inside the user area where the file should be made available."
    )

class StagingRequest(BaseModel):
    """Request model for staging data."""

    data: DataItem = Field(
        ...,
        description="Single data mapping with local and relative paths.",
        json_schema_extra={
            "example": {
                "local_path_on_storage": "/mnt/storage_a/data1",
                "relative_path": "project/data1"
            }
        },
    )

class SuccessResponse(BaseModel):
    """Successful response model."""
    status: str
    message: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "success",
                "message": "Data staged for user test_user with method local_copy"
            }
        }
    )

class ValidationError(BaseModel):
    """Validation error model."""
    detail: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "detail": "Source path does not exist: /mnt/storage_a/data1 or Invalid Staging method"
            }
        }
    )

# --------------------------- CONFIGURATION --------------------------------------------
def get_config():
    """Fetch the application configuration."""
    return {
        "source_storage_path": os.getenv("SOURCE_STORAGE_PATH", "/tmp/storage_a"),
        "target_storage_path": os.getenv("TARGET_STORAGE_PATH", "/tmp/user_areas"),
        "allowed_methods": json.loads(os.getenv("ALLOWED_METHODS", '["local_copy", "local_symlink"]')),
    }

# --------------------------- API ENDPOINT --------------------------------------------
@app.post(
    "/stage-data/",
    response_model=SuccessResponse,
    responses={
        400: {
            "model": ValidationError,
            "description": "Validation Error for Missing Path, Invalid Method, or Empty Data",
            "content": {
                "application/json": {
                    "examples": {
                        "missing_path": {
                            "summary": "Source Path Does Not Exist",
                            "value": {
                                "detail": "Source path does not exist: /mnt/storage_a/data1"
                            },
                        },
                        "invalid_method": {
                            "summary": "Invalid Staging Method",
                            "value": {
                                "detail": "Invalid staging method: invalid_method"
                            },
                        },
                        "empty_data": {
                            "summary": "Empty Data Array",
                            "value": {
                                "detail": "Data array must not be empty"
                            },
                        },
                    }
                }
            },
        },
        422: {
            "description": "Validation Error for Request Body or Parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["query", "method"],
                                "msg": "field required",
                                "type": "value_error.missing",
                            }
                        ]
                    }
                }
            },
        },
        500: {"description": "Internal Server Error"},
    },
)
# --------------------------- API ENDPOINT --------------------------------------------
@app.post("/stage-data/", response_model=SuccessResponse)
async def stage_data(
    request: StagingRequest,
    method: str = Query(..., description="The method to use for staging data."),
    username: str = Query(..., description="The username of the requester."),
    site_config: dict = Depends(get_config),
):
    logger.info(f"Received request with method={method}, username={username}, data={request.data}")
    if method not in site_config["allowed_methods"]:
        logger.warning(f"Invalid method: {method}")
        raise HTTPException(status_code=400, detail=f"Invalid staging method: {method}")

    # Ensure the user exists
    ensure_user_exists(username)

    # Load Source and Target storage
    source_storage = site_config['source_storage_path']
    target_storage = site_config['target_storage_path']
    logger.debug(f"Loaded Source Storage: {source_storage}")
    logger.debug(f"Loaded Target Storage: {target_storage}")
    # Create User Directory if it does not exist
    user_area = os.path.join(target_storage, username)
    os.makedirs(user_area, exist_ok=True)
    logger.debug(f"User area created: {user_area}")
    # Extract local path and target path
    local_path = os.path.join(source_storage, request.data.local_path_on_storage)
    target_path = os.path.join(user_area, request.data.relative_path)
    logger.debug(f"Processing {local_path} -> {target_path}")
    # Check if source exists
    if not os.path.exists(local_path):
        logger.error(f"Source path does not exist: {local_path}")
        raise HTTPException(status_code=400, detail=f"Source path does not exist: {local_path}")
    # Ensure the target directory exists
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    # Apply the chosen method
    if not os.path.exists(target_path):
        try:
            AVAILABLE_METHODS[method](local_path, target_path)
            logger.debug(f"Applied method {method} on {local_path}")
            # Set read-only
            set_read_only(target_path, username)
            logger.debug(f"Set read-only permissions for {target_path}")

        except HTTPException as e:
            logger.error(f"HTTPException: {e.detail}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

        logger.info(f"Data staged successfully for user {username} with method {method}")
        return {"status": "success", "message": f"Data staged for user {username} with method {method}"}
    else:
        logger.info(f"Data is already available at {target_path}")
        return {"status": "success", "message": f"Data already available at {target_path}"}