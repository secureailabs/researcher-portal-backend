# Install dependencies

poetry shell
poetry install

# TO RUN THE DEV SERVER LOCALLY

uvicorn app.main:server --host 0.0.0.0 --port 8000

# To run locally using Docker

1. make build_image
2. docker run -it -p 8001:8000 <docker image id>

# Deployment steps using Docker

1. make push_image
2. docker run -d -p 8001:8000 <docker image id>

# To login to the docker hub

docker login $DOCKER_REGISTRY_URL --username $DOCKER_REGISTRY_USERNAME --password $DOCKER_REGISTRY_PASSWORD
