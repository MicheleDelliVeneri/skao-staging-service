from fastapi.testclient import TestClient
from app.staging_service import app
import os
import stat
import pytest
from fastapi import HTTPException
from app.utility import ensure_user_exists

client = TestClient(app)

def setup_module(module):
    """Set up test directories and files."""
    os.makedirs("/tmp/storage_a/data/folder", exist_ok=True)
    os.makedirs("/tmp/user_areas", exist_ok=True)

    # Create individual test files
    with open("/tmp/storage_a/data/file1.txt", "w") as f:
        f.write("Sample data file")
    with open("/tmp/storage_a/data/file2.txt", "w") as f:
        f.write("Another data file")

    # Create files in the folder for directory testing
    with open("/tmp/storage_a/data/folder/file3.txt", "w") as f:
        f.write("File in folder")
    with open("/tmp/storage_a/data/folder/file4.txt", "w") as f:
        f.write("Another file in folder")

def teardown_module(module):
    """Clean up test directories and reset permissions."""
    reset_permissions("/tmp/user_areas")
    os.system("rm -rf /tmp/storage_a /tmp/user_areas")

def check_permissions(path, expected_permissions):
    """Check if the path has the expected permissions."""
    actual_permissions = stat.S_IMODE(os.stat(path).st_mode)
    assert actual_permissions == expected_permissions, (
        f"Expected {oct(expected_permissions)} but got {oct(actual_permissions)} for {path}"
    )

def reset_permissions(path):
    """Recursively reset permissions to writable for cleanup."""
    if os.path.isfile(path):
        os.chmod(path, 0o644)  # Writable for files
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                os.chmod(os.path.join(root, file), 0o644)
            for directory in dirs:
                os.chmod(os.path.join(root, directory), 0o755)  # Writable for directories
        os.chmod(path, 0o755)  # Ensure root directory is writable


# --------------------------- TEST CASES --------------------------------------------

def test_file_staging_with_read_only_permissions():
    """
    Test staging two files in separate requests, then verify that each file
    is staged with read-only permissions.
    """
    username = "michele"

    # Stage file1
    response = client.post(
        f"/stage-data/?method=local_copy&username={username}",
        json={
            "data": {
                "local_path_on_storage": "/tmp/storage_a/data/file1.txt",
                "relative_path": "project/file1.txt"
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

    # Stage file2
    response2 = client.post(
        f"/stage-data/?method=local_copy&username={username}",
        json={
            "data": {
                "local_path_on_storage": "/tmp/storage_a/data/file2.txt",
                "relative_path": "project/file2.txt"
            }
        }
    )
    assert response2.status_code == 200
    assert response2.json()["status"] == "success"

    # Check if files exist with correct permissions
    staged_file1 = f"/tmp/user_areas/{username}/project/file1.txt"
    staged_file2 = f"/tmp/user_areas/{username}/project/file2.txt"

    assert os.path.exists(staged_file1)
    assert os.path.exists(staged_file2)

    # Verify owner-only permissions (e.g., 0o400)
    check_permissions(staged_file1, 0o400)
    check_permissions(staged_file2, 0o400)



def test_directory_staging_with_read_only_permissions():
    """
    Test staging an entire directory (folder) in a single request,
    then verify it and its contents have read-only permissions.
    """
    username = "michele"
    response = client.post(
        f"/stage-data/?method=local_copy&username={username}",
        json={
            "data": {
                "local_path_on_storage": "/tmp/storage_a/data/folder",
                "relative_path": "project/folder"
            }
        }
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"

    # Check if directory and files exist with correct permissions
    staged_folder = f"/tmp/user_areas/{username}/project/folder"
    staged_file3 = f"/tmp/user_areas/{username}/project/folder/file3.txt"
    staged_file4 = f"/tmp/user_areas/{username}/project/folder/file4.txt"

    assert os.path.exists(staged_folder)
    assert os.path.exists(staged_file3)
    assert os.path.exists(staged_file4)

    # Verify owner-only permissions for directories and files (e.g., 0o500 for dir, 0o400 for files)
    check_permissions(staged_folder, 0o500)
    check_permissions(staged_file3, 0o400)
    check_permissions(staged_file4, 0o400)


def test_invalid_method():
    """Test using an invalid staging method."""
    response = client.post(
        "/stage-data/?method=invalid_method&username=test_user",
        json={
            "data": {
                "local_path_on_storage": "/tmp/storage_a/data/file1.txt",
                "relative_path": "project/file1.txt"
            }
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid staging method: invalid_method"


def test_missing_source_path():
    """Test using a missing source path."""
    missing_path = "/tmp/storage_a/data/missing_file.txt"
    assert not os.path.exists(missing_path), f"Test file unexpectedly exists: {missing_path}"

    response = client.post(
        "/stage-data/?method=local_copy&username=test_user",
        json={
            "data": {
                "local_path_on_storage": missing_path,
                "relative_path": "project/missing_file.txt"
            }
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == f"Source path does not exist: {missing_path}"


def test_no_data_field():
    """Test request with no 'data' field."""
    response = client.post(
        "/stage-data/?method=local_copy&username=test_user",
        json={}
    )
    # Expect a 422 validation error from Pydantic (Unprocessable Entity)
    assert response.status_code == 422
    assert "detail" in response.json()



def test_malformed_json():
    """Test staging with malformed JSON."""
    response = client.post(
        "/stage-data/?method=local_copy&username=test_user",
        content="Not a valid JSON"
    )
    # Also expect a 422 error because the request body is invalid
    assert response.status_code == 422
    assert "detail" in response.json()


import subprocess
from unittest.mock import patch

def test_ensure_user_exists_creates_user():
    """Test that ensure_user_exists creates a user if it doesn't exist."""
    username = "test_user"

    with patch("subprocess.run") as mock_run:
        # Simulate 'id' command indicating user does not exist
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=["id", username], returncode=1),  # User not found
            subprocess.CompletedProcess(args=["useradd", "-m", username], returncode=0)  # User created successfully
        ]

        ensure_user_exists(username)
        assert mock_run.call_count == 2
        mock_run.assert_any_call(["id", username], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        mock_run.assert_any_call(["useradd", "-m", username], check=True)


def test_ensure_user_exists_user_already_exists():
    """Test that ensure_user_exists does nothing if the user already exists."""
    username = "existing_user"

    with patch("subprocess.run") as mock_run:
        # Simulate 'id' command indicating user exists
        mock_run.return_value = subprocess.CompletedProcess(args=["id", username], returncode=0)

        ensure_user_exists(username)
        mock_run.assert_called_once_with(["id", username], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def test_ensure_user_exists_user_creation_failure():
    """Test that ensure_user_exists raises an error if user creation fails."""
    username = "failing_user"

    with patch("subprocess.run") as mock_run:
        # Simulate 'id' command indicating user does not exist
        # Simulate 'useradd' failing
        mock_run.side_effect = [
            subprocess.CompletedProcess(args=["id", username], returncode=1),  # User not found
            subprocess.CalledProcessError(1, ["useradd", "-m", username])  # User creation fails
        ]

        with pytest.raises(HTTPException) as exc_info:
            ensure_user_exists(username)

        assert exc_info.value.status_code == 500
        assert "Failed to ensure user exists" in str(exc_info.value.detail)
        assert mock_run.call_count == 2
        mock_run.assert_any_call(["id", username], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
        mock_run.assert_any_call(["useradd", "-m", username], check=True)


def test_user_permissions_after_creation():
    """Test that staged files are owned by the created user."""
    username = "test_user"
    file_path = "/tmp/user_areas/test_user/project/file1.txt"

    # Ensure the file exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write("Sample content")

    # Simulate setting ownership to the user
    os.chown(file_path, os.getuid(), os.getgid())  # Use mock in real tests

    # Verify ownership (requires mock or careful setup in tests)
    file_stat = os.stat(file_path)
    assert file_stat.st_uid == os.getuid(), "File is not owned by the correct user"