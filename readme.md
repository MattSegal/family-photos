# Family Photos

Currently at [memories.ninja](https://memories.ninja)

This app stores family photos in the cloud (AWS) and presents them in a static webpage.

Users can:

- browse photos
- upload photos
- download photos

## Implementation

[Zappa](https://github.com/Miserlou/Zappa#about)

## Setup

```
virtualenv env
pip install -r requirements.txt
# hack for Windows
mkdir ./env/Lib/site-packages/pillow 
zappa deploy/update dev
```

## TODO

* Download bucket contents (by album)

