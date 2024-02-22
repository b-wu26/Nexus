import boto3
import logging 
from botocore.exceptions import ClientError


class S3Client:

    def __init__(self):
        self.client = boto3.client("s3")


    def upload_file(self, file_obj, bucket="uw-nexus-contents", key=None):
        try:
            response = self.client.upload_fileobj(file_obj, bucket, key)
        except ClientError as e:
            logging.error(e)
            return False
        return response

    def get_file(self, bucket="uw-nexus-contents", key=None):
        try:
            response = self.client.get_object(Bucket=bucket, Key=key)
        except ClientError as e:
            logging.error(e)
            return False
        return response