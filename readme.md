# Family Photos

Currently at [memories.ninja](https://memories.ninja)

This app stores family photos in the cloud (AWS) and presents them in a static webpage.

Users can:

* browse photos
* upload photos


## To Do (prioritized)

* Padding at bottom of album
* Add login with Google OAuth to sign up / in
* Auto retry failed uploads
* Download bucket contents (by album)
* Prod db backups to s3 and local
* Dockerize?

## Deployment

Deployment is done using Ansible, which configures the server and pulls the latest code from the GitHubs repo's `master` branch. Secrets are AES encrypted in `deploy/secrets.yml`, an example unencrypted secrets file can be found at `deploy/secrets.example.yml`


## HTTPS

HTTPS is enabled via NGINX using the LetsEncrypt certbot for the certificate

Create cert

    certbot --nginx -d memories.ninja
    openssl dhparam -dsaparam -out /etc/ssl/certs/dhparam.pem 4096

Renew expiring cert

    certbot renew
