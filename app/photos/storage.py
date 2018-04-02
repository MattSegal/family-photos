from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class S3Boto3StaticStorage(S3Boto3Storage):
	"""
	Extend S3Boto3Storage to allow us to have a seperate bucket
	for media and static files
	"""
	bucket_name = settings.AWS_STATIC_STORAGE_BUCKET_NAME
