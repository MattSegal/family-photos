"""
Handle AWS events

Run to enable handlers in AWS
> zappa schedule dev
"""
from .image import resize_image


def image_upload(event, context):
     # Get the uploaded file's information
    key = event['Records'][0]['s3']['object']['key']
    filename = key.split('/')[-1]
    resize_image(filename)
