# Family Photos

Currently at

https://c1yj31x37l.execute-api.ap-southeast-2.amazonaws.com/dev/

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
* Ensure unique image names
