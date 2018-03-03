# Family Photos

Currently at [memories.ninja](https://memories.ninja)

This app stores family photos in the cloud (AWS) and presents them in a static webpage.

Users can:

* browse photos
* upload photos


## To Do (prioritized)

* Make upload bar text a little easier to read
* Display "0 successful, 0 failed" immediately
* Add better image viewing UI (left / right arrows, cross to exit, animation?)
* Padding at bottom of album
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

Deployment is done using Ansible, which configures the server and pulls the latest code from the GitHubs repo's `master` branch. Secrets are AES encrypted in `deploy/secrets.yml`, an example unencrypted secrets file can be found at `deploy/secrets.example.yml`
