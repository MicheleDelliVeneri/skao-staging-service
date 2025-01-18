# SKAO Staging Service

[![Qodana](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/MicheleDelliVeneri/skao-staging-service/actions/workflows/qodana_code_quality.yml)
[![codecov](https://codecov.io/gh/MicheleDelliVeneri/skao-staging-service/branch/main/graph/badge.svg?token=8MHP9PACXY)](https://codecov.io/gh/MicheleDelliVeneri/skao-staging-service)
A FastAPI service that stages data for SKAO analysis. This repository includes:

- **FastAPI** code in [`app/staging_service.py`](app/staging_service.py)
- **Tests** in [`tests/test_staging_service.py`](tests/test_staging_service.py)
- **Docker** configuration in [`Dockerfile`](Dockerfile)
- **Helm** chart in [`charts/my-staging-service/`](charts/my-staging-service/)

## Build the service 
1. Clone the repo: `git clone https://github.com/MicheleDelliVeneri/skao-staging-service.git`
2. Build the docker image: `docker build -t skao-staging-service:latest .`
3. Modify the Helm Chart values to reflect your configuration
4. Run the Helm Chart: `helm install skao-staging-service ./charts/skao-staging-service --set image.repository=skao-staging-service --set image.tag=latest
`
--------
### Optionally
5. (Minikube) Create Tunnel: `minikube service skao-staging-service --url`



