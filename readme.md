# Family Photos

Currently at [memories.ninja](https://memories.ninja)

This app stores family photos in the cloud (AWS) and presents them in a static webpage.

Users can:

- browse photos
- upload photos
- download photos


## TODO

* Download bucket contents (by album)
* Force rethumbnailing
* Offline thumbnailing
* Improve eagerness of image loading on page
* add better image viewing UI

## Deployment

/srv/app for Django app
/srv/env for virtualenv
/srv/static for staticfiles
/srv/gunicorn.log for gunicorn logs
