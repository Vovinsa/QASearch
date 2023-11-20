#!/bin/bash

check_swarm() {
    if docker info --format '{{.Swarm.LocalNodeState}}' | grep -q "active"; then
        echo "Docker Swarm is already initialized on $MANAGER_HOST"
    else
        echo "Docker Swarm is not initialized on $MANAGER_HOST. Initializing..."
        init_swarm
        join_workers
    fi
}

init_swarm() {
    manager_token=$(docker swarm init --advertise-addr "$MANAGER_HOST")
    echo "Docker Swarm initialized on $MANAGER_HOST as manager"
    echo "Manager token: $manager_token"
}

join_workers() {
    worker_hosts=$(echo "$HOSTS" | cut -d';' -f2-)

    for worker_host in $(echo "$worker_hosts" | tr ',' ' '); do
        worker_token=$(docker swarm join-token worker -q)
        docker swarm join --token "$worker_token" "$MANAGER_HOST":2377
        echo "Joined $worker_host as a worker"
    done
}

check_swarm
