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
- **Staing Methods code**: Located in ``app/staging_methods.py``
- **Tests**: Available in ``tests/test_staging_service.py``
- **Docker configuration**: Defined in ``Dockerfile``
- **Helm chart**: Found in ``charts/my-staging-service/``
- **React frontend**: Located in ``frontend/``
- **Sphinx docs**: In ``docs/``

The service is installed and configured with Helm and runs on a kubernates clusters.
The main objective of the service is to expose an API to perform
data transfers between locally mounted storages, a mounted storage
and an user Jupyter server, or through direct download.
The documentation is structured as follows:
    - :ref:`Overview`:
        gives an overview of the service at its components;
    - :ref:`Assumptions and Simplifications for the Demo`:
        outlines the assumptions and semplifications made for the working demo of the service
    - :ref:`Helm Deployment`:
        provides an overview of the Kubernetes components deployed using Helm and lists the configurable variables defined in the values.yaml file.
    - :ref:`API Schema`:
        outlines the logical flow of a FastAPI service that handles data staging operations.
    - :ref:`Api Documentation`:
        outlines the  documentation for every implemented method
    - :ref:`Building and Testing the SKAO Staging Service`:
        outlines how to build and test the service using minikube
    - :ref:`To Do List`:
        shows next development marks
    - :ref:`File Structure`:
        provides an overview of the SKAO Staging Service file structure.

.. toctree::
   :maxdepth: 2
   :caption: API Documentation:

   overview
   assumptions
   helm-deployment
   api-schema
   building-testing
   file-structure
   todo
   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`