# Family Photos

Currently at [memories.ninja](https://memories.ninja)

This app stores family photos in the cloud (AWS) and presents them in a static webpage.

Users can:

* browse photos
* upload photos

## To Do

* downloads
    - user can download their photos
    - user can download albumns
* users
    - login with google OAuth
    - photo owners
    - show / hide / soft delete photo
    - flag dated photos
* uploads
    - better upload validation (server side, client side)
    - more optimistic upload success
    - can browse or add more uploads while uploading
    - auto retry uploads
    - uploaded photos show nicer "not thumbnail" if not loading
    - ensure dedupe works
* thumbnailing
    - improve bounding box
* admin
    - replace 'review' page with admin commands
    - change timezone to Melbourne/Australia
    - album view
* display
    - order albumns by latest photo


## Deployment and hosting

Deployment and hosting are done using [this repo](https://github.com/MattSegal/swarm-infra).
