import uuid

from flask import request, jsonify
from . import app, s3_client

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/nexus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route("/api/<user_id>/feed_post/<course_id>", methods=["POST"])
def upload(user_id, course_id):
    if request.method == "POST":

        post_id = uuid.uuid4().hex        
        
        #TODO: where to store text content
        if (text := request.form["text_content"]) != "":
            pass
        else:
            return jsonify({"message": "Can not have empty text content"})

        file_key = None
        if request.files:
            print(f"User {user_id} attached a file with the post for {course_id}")
            file_to_upload = request.files["upload_file"]
            new_filename = uuid.uuid4().hex + '.' + file_to_upload.filename.rsplit('.', 1)[1].lower()
            
            if (type := request.form['type']) != "":
                file_key = f"{type.lower()}/{course_id}/{new_filename}"
                s3_client.upload_file(file_obj = file_to_upload, key = file_key)
            else:
                return jsonify({"message": "Error: undefined post type"})


        #TODO: put posting info in database

    
        response = {
            "message": "success",
            "user_id": user_id,
            "post_id": post_id,
            "course_id": course_id,
            "file_key": file_key
        }

        return jsonify(response)


@app.route("/feed/<user_id>", methods=["GET"])
def feed(user_id):
    
    #TODO: get list of all courses that this person is taking

    #TODO: get top X posts from each course

    #TODO: compile them into lists of posts with data that client(frontend) can use to generate feed

    pass

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