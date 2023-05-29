from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

# for storing static files like logos, css styles, etc


class StaticStorage(S3Boto3Storage):
    location = settings.AWS_LOCATION_S3
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

# For storing media files for storing user uploaded files


class PublicMediaStorage(S3Boto3Storage):
    location = settings.PUBLIC_MEDIA_LOCATION
    file_overwrite = False
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
