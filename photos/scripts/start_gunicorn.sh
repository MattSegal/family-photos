#!/bin/bash
NUM_WORKERS=3
DJANGO_WSGI_MODULE='photos.wsgi'

if [ "$1" == 'prod' ]
then
  echo "Using prod settings"
  export DJANGO_SETTINGS_MODULE='photos.settings.prod'
elif [ "$1" == 'staging' ]
then
  echo "Using staging settings"
  export DJANGO_SETTINGS_MODULE='photos.settings.staging'
elif [ "$1" == 'dev' ]
then
  echo "Using dev settings"
  export DJANGO_SETTINGS_MODULE='photos.settings.dev'
else
    echo "ERROR: Argument required, one of (prod, staging, dev)"
    exit 1
fi

echo "Starting photos app as `whoami`"

# Set DJANGO_SETTINGS_MODULE as global environment variable
regex='DJANGO_SETTINGS_MODULE=".\+"'
line="DJANGO_SETTINGS_MODULE=\"${DJANGO_SETTINGS_MODULE}\""
sed -i "s/$regex/$line/g" /etc/environment

echo "Activating virtualenv"
. /srv/env/bin/activate

echo "Installing requirements"
pip3 install -r /srv/app/requirements/prod.txt

echo "Running migrations"
/srv/app/manage.py migrate

echo "Installing requirements."
/srv/app/manage.py collectstatic --noinput

cd /srv/app/

# Use SIGKILL because gunicorn should be stopped already
echo "Stopping gunicorn if running"
pids="$(pgrep --exact gunicorn)";
if [[ "$pids" != "" ]];
then
  printf "$pids" | xargs kill -9;
fi

echo "Starting gunicorn in daemonized mode"
gunicorn photos.wsgi:application \
  --daemon \
  --name photos \
  --workers 3 \
  --capture-output \
  --log-level info \
  --log-file=/srv/gunicorn.log

# Use SIGKILL because celery should be stopped already
echo "Stopping celery working if running"
pids=$(pgrep --full 'celery worker')
if [[ "$pids" != "" ]]
then
  printf "$pids" | xargs kill -9
fi

echo "Starting celery worker in daemonized mode"
celery worker \
  --app photos \
  --loglevel info \
  --logfile /srv/celery.log \
  --detach

echo "Done"
