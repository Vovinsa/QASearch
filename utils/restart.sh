#!/bin/bash

echo "Building new images..."
bash utils/build.sh

echo "Removing gateway, embedder, ranker..."
docker service rm gateway embedder ranker

service_list=$(docker service ls --format "{{.Name}}" | grep '^service_')
first_service_name=$(echo "$service_list" | head -n 1)
data_generation="${first_service_name: -1}"

echo "Removing indexes services..."
docker service ls --format "{{.Name}}" | while read -r service_name; do
    if [[ $service_name == service_* ]]; then
        # Remove the Docker service
        echo "Removing service: $service_name"
        docker service rm "$service_name"
    fi
done

echo "Deploying indexes..."
bash utils/deploy_indexes.sh "$data_generation"

echo "Deploying new services..."
bash utils/deploy.sh
