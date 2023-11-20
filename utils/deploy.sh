#!/bin/bash

hosts_count=$(echo "$HOSTS" | tr ';' '\n' | wc -l)

echo "Deploying embedder..."
docker service create --name embedder --network qa-search-network --replicas 1 "$REGISTRY"/embedder:latest
echo "Done!"

echo "Deploying ranker..."
docker service create --name ranker --network qa-search-network --replicas 1 "$REGISTRY"/ranker:latest
echo "Done!"

echo "Deploying gateway..."
docker service create \
  --name gateway \
  --network qa-search-network \
  --replicas "$hosts_count" \
  -p 8000:8000 \
  --env REDIS_HOST="$REDIS_HOST" \
  --env REDIS_PORT="$REDIS_PORT" \
  --env REDIS_PASSWORD="$REDIS_PASSWORD" \
  "$REGISTRY"/gateway:latest

echo "Done!"