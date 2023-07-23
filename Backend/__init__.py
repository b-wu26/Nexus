from flask import Flask
from Backend.client.s3_client import S3Client

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/nexus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

s3_client = S3Client()
