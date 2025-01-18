import os
import os
import pwd
import grp
from fastapi import HTTPException

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