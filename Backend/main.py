import uuid
import boto3

from flask import Flask, request, render_template
from client.s3_client import S3Client

app = Flask(__name__)

# @app.route('/')
# def hello():
#     return '<h1>Hello, World!</h1>'

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file_to_upload = request.files["file-to-save"]

        new_filename = uuid.uuid4().hex + '.' + file_to_upload.filename.rsplit('.', 1)[1].lower()

        bucket_name = "uw-nexus-contents"

        # s3 = boto3.resource("s3")
        # s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)

        s3_client = S3Client()
        print(s3_client.upload_file(file_obj = file_to_upload, key = f"posts/{new_filename}"))
        
    return render_template("index.html")


# @api.route('/feed/<user_id>')
# def feed(user_id):
#     pass

# @api.route('/post/<post_id>')
# def show_post(post_id):
#     pass

# @api.route('/upload')
# def upload():
#     pass

# @api.route('/settings/<user_id>', methods = ['GET', 'POST', 'DELETE'])
# def settings(user_id):
#     if request.method == 'GET':

#     if request.method == 'POST':

#     if request.method == 'DELETE':