#!/bin/bash

is_registry_running() {
    docker inspect -f '{{.State.Running}}' registry 2>/dev/null
}

check_registry() {
  echo "Checking if docker registry exists on $REGISTRY..."
  if is_registry_running; then
    echo "Docker registry already exists"
  else
    echo "Docker registry does not exist. Creating..."
    create_registry
  fi
}

create_registry() {
  docker run -d -p "${REGISTRY#*:}":5000 --name registry registry:2
  echo "Docker registry created on $REGISTRY"
}

check_registry

echo "Build and push images to registry"

echo "Building embedder..."
docker build -t "${REGISTRY}"/embedder:latest embedder/
docker push "$REGISTRY"/embedder:latest

echo "Building ranker..."
docker build -t "$REGISTRY"/ranker:latest ranker/
docker push "$REGISTRY"/ranker:latest

echo "Building indexes..."
docker build -t "$REGISTRY"/indexes:latest indexes/
docker push "$REGISTRY"/indexes:latest

echo "Building gateway..."
docker build -t "$REGISTRY"/gateway:latest gateway/
docker push "$REGISTRY"/gateway:latest

echo "Pulling redis..."
docker pull docker.io/library/redis:latest

echo "Creating network..."
docker network create --driver overlay qa-search-network
echo "Done! Created qa-search-network"

echo "Done!"