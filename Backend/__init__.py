from flask import Flask
from Backend.client.s3_client import S3Client

app = Flask(__name__)
s3_client = S3Client()
