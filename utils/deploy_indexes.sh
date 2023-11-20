#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Provide DATA_GENERATION"
  exit 1
fi

data_generation=$1

echo "Starting redis..."
ssh root@"$REDIS_HOST" "docker run \
  -d \
  -p $REDIS_PORT:6379 \
  docker.io/library/redis:latest /bin/sh -c 'redis-server --requirepass $REDIS_PASSWORD'"

for (( i=0; i<4; i++ ))
do
  service_name="service_cluster${i}_dg${data_generation}"
  service_port=$((8002 + "$i"))

  echo "Creating service $service_name..."
  docker service create \
    --name "$service_name" \
    --replicas=1 \
    --network qa-search-network \
    --mount type=bind,source=/var/data,target=/var/data \
    --env CLUSTER="$i" \
    --env DATA_GENERATION="$data_generation" \
    --env REDIS_HOST="$REDIS_HOST" \
    --env REDIS_PORT="$REDIS_PORT" \
    --env REDIS_PASSWORD="$REDIS_PASSWORD" \
    --env SERVICE_NAME="$service_name" \
    --env SERVICE_PORT="$service_port" \
    "$REGISTRY"/indexes:latest

  echo "Cluster $i deployed"
done

echo "Done!"