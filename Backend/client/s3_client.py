import boto3
import logging 
from botocore.exceptions import ClientError


class S3Client:

    def __init__(self):
        self.client = boto3.client("s3")


    def upload_file(self, file_name, bucket, object_name=None):
        try:
            response = self.client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
