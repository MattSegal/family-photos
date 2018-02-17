#!/bin/bash
echo "Starting photos as `whoami`"

NUM_WORKERS=3
DJANGO_WSGI_MODULE='photos.wsgi'
# export PYTHONPATH=$DJANGODIR:$PYTHONPATH

if [ "$1" == 'prod' ]
then
    export DJANGO_SETTINGS_MODULE='photos.settings.prod'
else
    export DJANGO_SETTINGS_MODULE='photos.settings.dev'
fi

. /srv/env/bin/activate

if [ "$2" == 'deploy' ]
then
    pip3 install -r /srv/app/requirements/prod.txt
    /srv/app/manage.py migrate
fi

cd /srv/app/
gunicorn photos.wsgi:application \
  --daemon \
  --name photos \
  --workers 3 \
  --log-level=debug \
  --log-file=/srv/gunicorn.log
