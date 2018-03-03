#!/bin/bash
echo "Starting photos app as `whoami`"

NUM_WORKERS=3
DJANGO_WSGI_MODULE='photos.wsgi'

if [ "$1" == 'prod' ]
then
    echo "Using prod settings"
    export DJANGO_SETTINGS_MODULE='photos.settings.prod'
else
    echo "Using dev settings"
    export DJANGO_SETTINGS_MODULE='photos.settings.dev'
fi

echo "Activating virtualenv"
. /srv/env/bin/activate

echo "Installing requirements"
pip3 install -r /srv/app/requirements/prod.txt

echo "Running migrations"
/srv/app/manage.py migrate

echo "Installing requirements."
/srv/app/manage.py collectstatic --noinput

cd /srv/app/

echo "Stopping gunicorn if running"
ps auxww | grep 'gunicorn' | awk '{print $2}' | xargs kill -9

echo "Starting gunicorn in daemonized mode"
gunicorn photos.wsgi:application \
  --daemon \
  --name photos \
  --workers 3 \
  --capture-output \
  --log-level info \
  --log-file=/srv/gunicorn.log

echo "Stopping celery working if running"
ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9

echo "Starting celery worker in daemonized mode"
celery worker \
  --app photos \
  --loglevel info \
  --logfile /srv/celery.log \
  --detach

echo "Done"
