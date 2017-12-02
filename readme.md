# Family Photos

This app stores family photos in the cloud (AWS) and presents them in a static webpage.

Users can:

- browse photos
- upload photos
- download photos

## Implementation

[Zappa](https://github.com/Miserlou/Zappa#about)

* file upload adds file to S3, transforms file and adds to S3, then updates index


## Setup

```
pip install -r requirements.txt
zappa deploy dev
```