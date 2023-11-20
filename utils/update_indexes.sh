#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Provide DATA_GENERATION parameter"
  exit 1
fi

data_generation=$1

services=$(docker service ls --format "{{.Name}}" | grep "service_")

service_port=8002

for service in $services
do
  cluster=$(echo "$service" | grep -oP 'cluster(\d+)' | grep -oP '\d+')
  updated_service_name="service_cluster${cluster}_dg${data_generation}"
  if docker service ls | grep -q "$updated_service_name"; then
    echo "Service $updated_service_name is running"
  else
    echo "Service $updated_service_name doesn't exists. Creating..."
    docker service create \
      --name "$updated_service_name" \
      --replicas=1 \
      --network qa-search-network \
      --mount type=bind,source=/var/data,target=/var/data \
      --env CLUSTER="$cluster" \
      --env DATA_GENERATION="$data_generation" \
      --env REDIS_HOST="$REDIS_HOST" \
      --env REDIS_PORT="$REDIS_PORT" \
      --env REDIS_PASSWORD="$REDIS_PASSWORD" \
      --env SERVICE_NAME="$updated_service_name" \
      --env SERVICE_PORT="$service_port" \
      "$REGISTRY"/indexes:latest

    service_port=$(("$service_port" + 1))

    sleep 15

    echo "Updated service $updated_service_name deployed"

    redis-cli -h "$REDIS_HOST" -p "$REDIS_PORT" -a "$REDIS_PASSWORD" del "$service"
    docker service rm "$service"
  fi
done

echo "Done!"