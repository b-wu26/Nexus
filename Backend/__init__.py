from flask import Flask
from .client.s3_client import S3Client
from .models import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/nexus"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app=app)

s3_client = S3Client()
