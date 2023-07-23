import uuid
import boto3

from flask import Flask, request, render_template, jsonify
from client.s3_client import S3Client

s3_client = S3Client()

app = Flask(__name__)

# @app.route('/')
# def hello():
#     return '<h1>Hello, World!</h1>'

@app.route("/api/<user_id>/feed_post/<course_id>", methods=["POST"])
def upload(user_id, course_id):
    if request.method == "POST":

        post_id = uuid.uuid4().hex        
        file_key = None

        if request.files:
            print(f"User {user_id} attached a file with the post for {course_id}")
            file_to_upload = request.files["upload_file"]
            new_filename = uuid.uuid4().hex + '.' + file_to_upload.filename.rsplit('.', 1)[1].lower()
            
            if (type := request.form['type']) != "":
                file_key = f"{type.lower()}/{course_id}/{new_filename}"
                s3_client.upload_file(file_obj = file_to_upload, key = file_key)
            else:
                print("Error: undefined post type")
                return jsonify({"message": "fail"})

        #TODO: put posting info in database

    
        response = {
            "message": "success",
            "user_id": user_id,
            "post_id": post_id,
            "course_id": course_id,
            "file_key": file_key
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