. /srv/env/bin/activate
cd /srv/app
./manage.py runserver \
    --settings photos.settings.dev \
    0.0.0.0:8080
