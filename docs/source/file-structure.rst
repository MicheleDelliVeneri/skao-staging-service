.. _File Structure:

File Structure
==============

This section provides an overview of the SKAO Staging Service file structure.

Project Layout
--------------

::

    skao-staging-service/
    ├── app/
    │   ├── __init__.py
    │   ├── database.py
    │   ├── staging_methods.py
    │   ├── utility.py
    │   ├── jupyter_helper.py
    ├── charts/
    │   ├── skao-staging-service/
    │   │   ├── Chart.yaml
    │   │   ├── values.yaml
    │   │   ├── templates/
    │   │       ├── deployment.yaml
    │   │       ├── service.yaml
    │   │       ├── ingress.yaml
    ├── tests/
    │   ├── test_staging_service.py
    ├── docs/
    │   ├── source/
    │   │   ├── index.rst
    │   │   ├── conf.py
    ├── Dockerfile
    ├── README.md
    ├── requirements.txt

Description of Directories
--------------------------

- **app/**: Core application logic, including APIs and database models.
- **charts/**: Helm chart definitions for Kubernetes deployment.
- **tests/**: Unit and integration tests for the application.
- **docs/**: Documentation source files for Sphinx.
- **Dockerfile**: Docker build instructions for the application.