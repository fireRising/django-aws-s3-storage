from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class PrivateMediaStorage(S3Boto3Storage):
    location = 'media/private'
    default_acl = 'private'
    file_overwrite = True
    custom_domain = False


