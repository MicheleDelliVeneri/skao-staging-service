.. _Building and Testing the SKAO Staging Service:

Building and Testing the SKAO Staging Service
----------

Build the Service
*******
0. **Create a tunnel (Minikube)**:
   If using Minikube, create a tunnel to expose the service:

   .. code-block:: bash

      minikube service skao-staging-service --url

1. **Clone the repository**:

   .. code-block:: bash

      git clone https://github.com/MicheleDelliVeneri/skao-staging-service.git

2. **Build the Docker image**:

   .. code-block:: bash

      docker build -t skao-staging-service:latest .

3. **Modify the Helm Chart values**:
   Adjust the `values.yaml` file to reflect your specific configuration requirements.

4. **Install the Helm Chart**:

   .. code-block:: bash

      helm install skao-staging-service ./charts/skao-staging-service \
          --set image.repository=skao-staging-service \
          --set image.tag=latest

5. **Access the frontend**:
   Navigate to the service URL obtained via:

   .. code-block:: bash

      minikube service skao-staging-service --url

6. **Explore Service docs**:
    Navigate to `minikube_url/docs` to check the Docs Page,
    an interactive and auto-generated documentation interface
    provided by FastAPI, built using Swagger UI.

Testing the Service
******
1. **Set up local directories**:
    Create two directories on your host machine:
        - One for simulating the local storage.
        - Another for simulating the target user area.

2. **Configure Helm values**:
    Update the `values.yaml` file:
        - Set `storage.source.local.hostPath` to the local storage directory.
        - Set `userArea.source.local.hostPath` to the target user area directory.

3. **Create a file**:
    Use the File Creation Tool in the frontend to create a test file.

4. **Stage the file**:
    Use your preferred staging method to move the created file. This operation
    can be perfomed through the GUI or by sumbimitting a staging request through the FastAPI docs
    As an example:

    .. code-block:: json

      {
        "data": {
          "local_path_on_storage": "/mnt/storage_a/File1.txt",
          "relative_path": "File1Copy.txt"
        }
      }
5. **Check the file copy**

    .. code-block:: bash

        kubectl get pods
        kubectl exec -it skao-staging-service-pod -- ls -la /mnt/storage_b/user_areas/File1Copy.txt
