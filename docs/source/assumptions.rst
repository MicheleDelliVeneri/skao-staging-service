.. _Assumptions and Simplifications for the Demo:

Assumptions and Simplifications for the Demo
-----

To create a functional demo of the service, several underlying assumptions about data operations conducted prior to receiving the data staging request are made. These assumptions are as follows:

1. It is assumed that a functional Identity and Authentication Manager (IAM) is in place to authenticate and authorize the user for accessing or moving data.
2. The data is presumed to have been successfully transferred between sites and is accessible and readable at the specified local_path_on_storage.
3. Consistency in UID/GID across sites is assumed, or this information is provided by the IAM.

The service assumes that:

1. local_path_on_storage resides on storage_A. user_area/relative_path is located on storage_B. Here, storage_A and storage_B refer to external or local storages connected to the Kubernetes cluster and mountable as Kubernetes Volumes or PersistentVolumes.
2. It is assumed that the JupyterServer is reachable by the service, and a preconfigured token is available. This token must allow the service to query user information, start and stop servers, and copy data into the user's working directory.
