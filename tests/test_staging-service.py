from fastapi.testclient import TestClient
from app.staging_service import app
import os

client = TestClient(app)

def setup_module(module):
    os.makedirs("/tmp/storage_a/data", exist_ok=True)
    os.makedirs("/tmp/user_areas", exist_ok=True)
    with open("/tmp/storage_a/data/file1.txt", "w") as f:
        f.write("Sample data file")
    with open("/tmp/storage_a/data/file2.txt", "w") as f:
        f.write("Another data file")

def teardown_module(module):
    os.system("rm -rf /tmp/storage_a /tmp/user_areas")

def test_staging_method_1():
    response = client.post(
        "/stage-data/",
        json={
            "data": [
                {"local_path_on_storage": "/tmp/storage_a/data/file1.txt", "relative_path": "project/file1.txt"},
                {"local_path_on_storage": "/tmp/storage_a/data/file2.txt", "relative_path": "project/file2.txt"}
            ],
            "method": "method_1",
            "username": "test_user"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Data staged successfully"}
    assert os.path.exists("/tmp/user_areas/test_user/project/file1.txt")
    assert os.path.exists("/tmp/user_areas/test_user/project/file2.txt")