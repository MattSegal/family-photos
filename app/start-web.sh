#!/bin/bash
echo "Starting photos app as `whoami`"

echo "Running migrations"
./manage.py migrate

echo "Collecting static files (background job)"
./manage.py collectstatic --noinput &

mkdir -p /var/log/gunicorn

echo "Starting gunicorn"
gunicorn photos.wsgi:application \
  --name photos \
  --workers 3 \
  --bind 0.0.0.0:8000 \
  --capture-output \
  --log-level info \
  --error-logfile /var/log/gunicorn/error.log \
  --access-logfile /var/log/gunicorn/access.log
