#!/bin/bash
# Script to back up database.
set -e

export $(grep -v '^#' env/.env.prod | xargs)

if [ -z "$HOST" ]
then
    echo "\n>>> Error: HOST environment variable must be set."
    exit 1
fi
if [ -z "$PGDATABASE" ]
then
    echo "\n>>> Error: PGDATABASE environment variable must be set."
    exit 1
fi

TIME=$(date "+%s")
BUCKET_NAME="swarm-db-backup/photos"
BACKUP_FILE="postgres_${PGDATABASE}_${TIME}.sql.gz"
BACKUP_LOCAL_FILE="/srv/backups/$BACKUP_FILE"
BACKUP_S3_DIR="s3://${BUCKET_NAME}"
BACKUP_S3_FILE="s3://${BUCKET_NAME}/${BACKUP_FILE}"

echo -e "\n>>> Creating backup directory"
chmod 400 infra/id_rsa
ssh -o StrictHostKeyChecking=no -i infra/id_rsa lab@$HOST mkdir -p /srv/backups/

echo -e "\n>>> Taking backup on $HOST"
ssh -o StrictHostKeyChecking=no -i infra/id_rsa lab@$HOST \
    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    /bin/bash << EOF
    set -e
    export PGHOST=/var/run/postgresql
    export PGDATABASE=$PGDATABASE
    export PGUSER=$PGUSER
    export PGPASSWORD=$PGPASSWORD

    echo -e "\n>>> Creating local database dump $BACKUP_LOCAL_FILE"
    pg_dump --format=custom | gzip > $BACKUP_LOCAL_FILE

    echo -e "\n>>> Copying local dump to S3 - $BACKUP_S3_DIR"
    aws s3 cp $BACKUP_LOCAL_FILE $BACKUP_S3_FILE

    echo -e "\n>>> Latest S3 backup:"
    aws s3 ls $BACKUP_S3_DIR --recursive | sort | tail -n 1    

    echo -e "\n>>> Backup completed."
EOF
