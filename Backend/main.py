import uuid
import boto3

from flask import Flask, request, render_template, jsonify
from client.s3_client import S3Client

app = Flask(__name__)

# @app.route('/')
# def hello():
#     return '<h1>Hello, World!</h1>'

@app.route("/api/<user_id>/feed_post/<course_id>", methods=["POST"])
def upload(user_id, course_id):
    if request.method == "POST":
        
        post_id = uuid.uuid4().hex
        file_to_upload = request.files["upload-file"]

        new_filename = uuid.uuid4().hex + '.' + file_to_upload.filename.rsplit('.', 1)[1].lower()

        #put posting info in database

        # Commented out for now, since we know it already works. Dont wanna waste random calls
        # s3_client = S3Client()
        # print(s3_client.upload_file(file_obj = file_to_upload, key = f"posts/{new_filename}"))
        response = {
            "success": True,
            "user_id": user_id,
            "post_id": post_id,
            "course_id": course_id,
            "file_name": new_filename
        }
        return jsonify(response)


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