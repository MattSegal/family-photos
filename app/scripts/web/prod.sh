#!/bin/bash
set -e
echo "Running migrations"
./manage.py migrate

echo "Starting gunicorn"
gunicorn photos.wsgi:application \
    --name photos \
    --preload \
    --workers 1 \
    --threads 2 \
    --bind 0.0.0.0:8000
