#!/bin/bash
# Script to deploy.
set -e
export $(grep -v '^#' env/.env.prod | xargs)

echo -e "\n>>> Deploying Docker Stack $DOCKER_STACK_NAME to $HOST"
DEPLOY_DIR="/srv/deploy/$(date +%s)"

echo -e "\n>>> Creating deployment directory $DEPLOY_DIR"
chmod 400 infra/id_rsa
ssh -o StrictHostKeyChecking=no -i infra/id_rsa lab@$HOST mkdir -p $DEPLOY_DIR

scp -o StrictHostKeyChecking=no -i infra/id_rsa \
    docker/docker-compose.prod.yml \
    lab@$HOST:${DEPLOY_DIR}/docker-compose.prod.yml

scp -o StrictHostKeyChecking=no -i infra/id_rsa \
    env/.env.prod \
    lab@$HOST:${DEPLOY_DIR}/.env.prod

echo -e "\n>>> Updating Docker Swarm stack $DOCKER_STACK_NAME"
ssh -o StrictHostKeyChecking=no -i infra/id_rsa lab@$HOST /bin/bash << EOF
    set -e
    cd $DEPLOY_DIR
    echo "$DOCKER_PASSWORD" | docker login --username $DOCKER_ID --password-stdin
    docker stack deploy --with-registry-auth --compose-file docker-compose.prod.yml $DOCKER_STACK_NAME
EOF

echo -e "\n>>> Deployment finished"
