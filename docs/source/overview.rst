.. _Overview:

Overview
--------
.. image:: images/staging-service-schema.png
    :alt: Staging Service Schema
    :align: center

The main components of the service are:

1. The SKAO Staging Service: constituted by the **FastAPI** backend and a **React Frontend**.
The service provides a POST API endpoint at `service_url/stage_data`. This endpoint accepts the following inputs:
    - Query Parameters:
        method: Specifies the staging method to be used.
        username: The name of the user initiating the staging request.
    - Request Body (JSON):
        local_path_on_storage: The source path of the data to be staged.
        relative_path: The destination path relative to the user's storage area.
The API processes these inputs to perform the requested staging operation with the selected `Method`.
In case the data is not available, or the method is not compatible with those implemented at the site where the
service is hosted, the API returns an Error. At this moment the following staging methods have been implemented:

    - local_copy:
        moves data between locally mounted `local_path_on_storage` and `user_area\relative_path` with the unix `cp` command;
    - symlink_copy:
        creates a hard link between the `local_path_on_storage`  and `user_area\relative_path`;
    - direct_dowload:
        serves the `local_path_on_storage` file as an HTTP response through the FastAPI `FileResponse`.
        It thus provides a direct browser link to download the file on the user machine;
    - jupyter_copy:
        copies the `local_path_on_storage` in the  `JupyterServer` user working directory at the path
        `working_directory\relative_path`. This is done by checking Jupyter Server status, starting the user server in case
        is down, and copying the data on `local_path_on_storage` through a PUT request.

The service performs several checks and actions to ensure safe and efficient file operations:
    - Pre-Copy Checks:
        File Availability in local_path_on_storage: Before initiating any copy operation, the service verifies that the file exists at the specified local_path_on_storage. If the file is not available, the operation is aborted, and an appropriate error is returned to the client.
    - File Duplication Check:
        The service checks if the file already exists in the target location, as specified by the relative_path. If the file is already present, the copy operation is skipped, and a success response is returned indicating no further action was needed.
    - Copy Operation:
        If both checks pass, the file is copied from the source (local_path_on_storage) to the destination (relative_path) on the target storage or user's environment.
    - Post-Copy Action:
        Once the copy operation is successfully completed, the service sets the copied file to read-only for the user. This ensures the integrity of the data and prevents unintended modifications.


The service also includes a frontend interface that provides the following functionality:
    - Data Staging:
        A user-friendly interface to perform the POST call to the stage_data API, allowing users to specify the staging method, username, and paths interactively.
    - Log Viewer:
        Displays real-time logs of the service, enabling users to monitor the system's operations and troubleshoot issues.
    - File Creation:
        A tool to create files directly on the local storage, simplifying testing and validation of the service's functionality.

This frontend enhances the usability of the API by providing an intuitive interface for staging data, viewing logs, and testing the service.
See the image below for a visual representation of the interface.

.. image:: images/frontend.png
    :alt: Frontend
    :align: center

2. The MySQL database backend is used to store information about data staging operations. Upon initialization, the database schema is set up, and for every data staging operation—regardless of whether it succeeds or fails—a record is inserted into the database with the following details:
    - id: A unique identifier for the operation.
    - local_path_on_storage: The source path of the file being staged.
    - relative_path: The target path relative to the user area.
    - status: The outcome of the operation (e.g., success or failure).
    - error_reason: A description of the reason for failure, if applicable.

The application maintains detailed logging of all operations in a dedicated log file.
Each operation, including data staging requests, file checks, and copy actions, is recorded with relevant
details. This logging provides a comprehensive history of all activities,
facilitating troubleshooting and auditing.

Key Points About Logging:

- Operation Details:
    The logs capture key information, such as the method invoked, user details, paths involved, and operation outcomes.
- Error Tracking:
    Any errors or exceptions encountered during the operations are logged, including stack traces when available, to assist in diagnosing issues.
- Log File Location:
    The log file is created and maintained in the application directory by default (e.g., staging_service.log).
- Log Levels:
    The logging system supports multiple levels, such as INFO, DEBUG, WARNING, and ERROR. This enables filtering logs based on the desired level of detail.

By logging every operation to a file, the application ensures transparency and provides administrators with the tools needed to monitor the service and address potential issues effectively.