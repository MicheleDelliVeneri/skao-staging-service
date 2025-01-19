Skao Staging Service Documentation
==================================

*"To Boldly go where no staging service has gone before*

*MDV 20/01/25 - 2 AM "*

------

Welcome to the skao-staging-service documentation.
This service stages data for SKAO analysis.
The service code is distributed through GitHUb and available at the following
`Link <https://github.com/MicheleDelliVeneri/skao-staging-service>`_

Below are the main components and features of the repository:

- **FastAPI code**: Located in ``app/staging_service.py``
- **Tests**: Available in ``tests/test_staging_service.py``
- **Docker configuration**: Defined in ``Dockerfile``
- **Helm chart**: Found in ``charts/my-staging-service/``
- **React frontend**: Located in ``frontend/``
- **Sphinx docs**: In ``docs/``

The service is installed and configured with Helm and runs on a kubernates clusters.
The main objective of the service is to perform
data transfers between locally mounted storages or a mounted storage
and an user Jupyter server working directory.

Overview
--------
.. image:: images/staging-service-schema.png
    :alt: Staging Service Schema
    :align: center

The main components of the service are:

1. The SKAO Staging Service: constituted by the **FastAPI** backend and a **React Frontend**.
The service provides a POST API endpoint at service_url/stage_data. This endpoint accepts the following inputs:
    - Query Parameters:
        method: Specifies the staging method to be used.
        username: The name of the user initiating the staging request.
    - Request Body (JSON):
        local_path_on_storage: The source path of the data to be staged.
        relative_path: The destination path relative to the user's storage area.
The API processes these inputs to perform the requested staging operation.

The service also includes a frontend interface that provides the following functionality:
    - Data Staging: A user-friendly interface to perform the POST call to the stage_data API, allowing users to specify the staging method, username, and paths interactively.
    - Log Viewer: Displays real-time logs of the service, enabling users to monitor the system's operations and troubleshoot issues.
    - File Creation: A tool to create files directly on the local storage, simplifying testing and validation of the service's functionality.

This frontend enhances the usability of the API by providing an intuitive interface for staging data, viewing logs, and testing the service.
See the image below for a visual representation of the interface.

.. image:: images/frontend.png
    :alt: Frontend
    :align: center



2. The MySQL databse backend


Helm Deployment Schema
**********

.. image:: images/helm-layout.png
    :alt: Helm Deployment Schema
    :align: center

The service relies on some underlying assumptions:

1. There is a functioning Identity and Authentication Manager (IAM) which has authenticated the user
and given authorization to accecss / move the data
2. That the data has been moved to


API Schema
**********

.. image:: images/logical-flow.png
    :alt: Application Flow
    :align: center


Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`