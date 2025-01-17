# SKAO Staging Service

[![Qodana](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/qodana_code_quality.yml)
[![codecov](https://codecov.io/gh/MicheleDelliVeneri/skao-staging-service/branch/main/graph/badge.svg?token=8MHP9PACXY)](https://codecov.io/gh/MicheleDelliVeneri/skao-staging-service)
[![Documentation Status](https://readthedocs.org/projects/skao-staging-service/badge/?version=latest)](https://skao-staging-service.readthedocs.io/en/latest/?badge=latest)
[![Unit Tests](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/unit-tests.yml)
[![Docker Tests](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/docker-tests.yml/badge.svg)](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/docker-tests.yml)
[![Qodana](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/qodana_code_quality.yml)
[![Helm Tests](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/helm-tests.yml/badge.svg)](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/helm-tests.yml)
[![Helm Integration Tests with Kind](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/kind-integration-test.yml/badge.svg)](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/kind-integration-test.yml)


for SKAO analysis. This repository includes:

- **FastAPI** code in [`app/staging_service.py`](app/staging_service.py)
- **Tests** in [`tests/test_staging_service.py`](tests/test_staging_service.py)
- **Docker** configuration in [`Dockerfile`](Dockerfile)
- **Helm** chart in [`charts/my-staging-service/`](charts/my-staging-service/)
- **React** frontend in [`frontend/`](frontend/)
- **Sphinx** docs in  [`docs/`](docs/)

For a complete description of the service, and its use check our documentation on
[Read The Docs](https://skao-staging-service.readthedocs.io/en/latest/).
The service is run in a Kubernates Cluster and it is installed and configured with Helm. 

## Build the service 
1. Clone the repo: `git clone https://github.com/MicheleDelliVeneri/skao-staging-service.git`
2. configure your shell environment so that Docker commands run on your local machine interact with the Docker daemon inside the Minikube virtual machine, rather than the Docker daemon on your local host `eval $(minikube docker-env)
`
3. Build the docker image: `docker build -t skao-staging-service:latest .`
3. Modify the Helm Chart values to reflect your configuration
4. Run the Helm Chart: `helm install skao-staging-service ./charts/skao-staging-service --set image.repository=skao-staging-service --set image.tag=latest
`
5. (Minikube) Create Tunnel: `minikube service skao-staging-service --url`

## Test The Service with FastAPI Tests
1. Create two local directories on the Host Machine, one for simulating the local storage, and another to simulate the target user area. These will be mounted in the application pod.
2. Set the paths of the two directories in the Helm Values.yaml file, one as the `storage.source.local.hostPath` and the other as the `userArea.source.local.hostPath`
3. Create a file inside the app pod `kubectl exec -it skao-staging-service-7fd6664978-8fml5  -- sh -c "echo 'This is File1.txt' > /mnt/storage_a/File1.txt".` or use the frontend tool 
This file simulates the file that the user want to stage from the local storage to its user area. 
4. Navigate to `http:127.0.0.1:MINIKUBEPORT/docs` where MINIKUBEPORT is the port obtained in step 5. 
5. Set method to `local_copy`, set your `username` and add the following request body:
    ``` 
    {
      "data": {
        "local_path_on_storage": "/mnt/storage_a/File1.txt",
        "relative_path": "File1Copy.txt"
      }
    }
    ```
    You should see a succesful response 
    ```
    {
    "status": "success",
    "message": "Data staged for user michele with method local_copy"
    }
6. Check the file copy 
    ```
    kubectl get pods
    kubectl exec -it skao-staging-service-pod -- ls -la /mnt/storage_b/user_areas/File1Copy.txt
    ```
   


## Test The Service with Frontend
1. Navigate to the url provided by `minikube service skao-staging-service --url`
2. Create a File with the FileCreation Tool 
3. Use your favorite staging method to move the created file
# Helm Chart Guide

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: latest](https://img.shields.io/badge/AppVersion-latest-informational?style=flat-square)

A Helm chart for deploying the SKAO staging service

## Maintainers

| Name | Email | Url |
| ---- | ------ | --- |
| Michele | <micheledelliveneri@gmail.com> |  |

## Source Code

* <https://github.com/MicheleDelliVeneri/skao-staging-service>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| config.allowedMethods[0] | string | `"local_copy"` |  |
| config.allowedMethods[1] | string | `"local_symlink"` |  |
| config.allowedMethods[2] | string | `"direct_download"` |  |
| config.allowedMethods[3] | string | `"jupyter_copy"` |  |
| config.jupyterHubUrl | string | `"https://jupyterhub"` |  |
| config.rucioBaseUrl | string | `"https://rucio-instance"` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"skao-staging-service"` |  |
| image.tag | string | `"latest"` |  |
| ingress.annotations."nginx.ingress.kubernetes.io/rewrite-target" | string | `"/"` |  |
| ingress.enabled | bool | `true` |  |
| ingress.hosts[0].host | string | `"staging-service.local"` |  |
| ingress.hosts[0].paths[0].path | string | `"/"` |  |
| ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| ingress.hosts[0].paths[1].path | string | `"/logs"` |  |
| ingress.hosts[0].paths[1].pathType | string | `"ImplementationSpecific"` |  |
| ingress.tls | list | `[]` |  |
| logging.level | string | `"DEBUG"` |  |
| replicaCount | int | `2` |  |
| service.port | int | `8000` |  |
| service.type | string | `"NodePort"` |  |
| storage.source.ceph.enabled | bool | `false` |  |
| storage.source.ceph.options | string | `"name=admin,secret=<secret>,rw"` |  |
| storage.source.ceph.path | string | `"/mnt/source-ceph"` |  |
| storage.source.ceph.server | string | `"ceph-source.example.com"` |  |
| storage.source.local.enabled | bool | `true` |  |
| storage.source.local.hostPath | string | `"/Volumes/FastStorage/storage_a"` |  |
| storage.source.local.path | string | `"/mnt/storage_a"` |  |
| storage.source.nfs.enabled | bool | `false` |  |
| storage.source.nfs.path | string | `"/mnt/source-nfs"` |  |
| storage.source.nfs.server | string | `"nfs-source.example.com"` |  |
| storage.source.nfs.serverPath | string | `"/source-nfs-exported-path"` |  |
| storage.source.type | string | `"local"` |  |
| storage.userArea.ceph.enabled | bool | `false` |  |
| storage.userArea.ceph.options | string | `"name=admin,secret=<secret>,rw"` |  |
| storage.userArea.ceph.path | string | `"/mnt/user-area-ceph"` |  |
| storage.userArea.ceph.server | string | `"ceph-user-area.example.com"` |  |
| storage.userArea.local.enabled | bool | `true` |  |
| storage.userArea.local.hostPath | string | `"/Volumes/FastStorage/user_areas"` |  |
| storage.userArea.local.path | string | `"/mnt/user_areas"` |  |
| storage.userArea.nfs.enabled | bool | `false` |  |
| storage.userArea.nfs.path | string | `"/mnt/user-area-nfs"` |  |
| storage.userArea.nfs.server | string | `"nfs-user-area.example.com"` |  |
| storage.userArea.nfs.serverPath | string | `"/user-area-nfs-exported-path"` |  |
| storage.userArea.type | string | `"local"` |  |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.14.2](https://github.com/norwoodj/helm-docs/releases/v1.14.2)