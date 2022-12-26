#!/bin/bash
# Script to deploy.
set -e
HOST='167.179.136.207'
REPO="photos"
ssh root@$HOST /bin/bash << EOF
    set -e
    cd /root/repos/$REPO
    echo "Cleaning $REPO git repository"
    git reset --hard
    git clean -dfx
    git checkout master
    git pull
    echo "Building $REPO"
    pushd frontend
    yarn install
    yarn build
    popd
    echo "Building Docker image for $REPO"
    docker build -t $REPO:latest -f docker/Dockerfile .
    echo "Deploying $REPO to docker swarm"
    docker stack deploy --compose-file docker/docker-compose.prod.yml $REPO
EOF
