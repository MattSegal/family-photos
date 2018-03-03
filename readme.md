# Family Photos

Currently at [memories.ninja](https://memories.ninja)

This app stores family photos in the cloud (AWS) and presents them in a static webpage.

Users can:

- browse photos
- upload photos


## To Do (prioritized)

* Make upload bar text a little easier to read
* Display "0 successful, 0 failed" immediately
* Add better image viewing UI (left / right arrows, cross to exit, animation?)
* Figure out how to use celery locally
* Force rethumbnailing
* Improve eagerness of image loading on page
* Try reduce quality of large images slightly
* Add login with Google OAuth to sign up / in
* Auto retry failed uploads
* Download bucket contents (by album)
* Prod db backups to s3 and local
* Dockerize?

## Deployment

/srv/app for Django app
/srv/env for virtualenv
/srv/static for staticfiles
/srv/photos for temp local photo storage
/srv/gunicorn.log for gunicorn logs
/srv/celery.log for celery logs
