import uuid
from datetime import datetime
from models import db

from flask import Blueprint, request, jsonify

from models.student_profile import student_profile
from models.class_profile import class_profile
from models.schedule import schedule
from models.post import post
from models.notes_and_more import notes_and_more

from client.s3_client import S3Client

post_endpoints = Blueprint("post_endpoints", __name__)
s3_client = S3Client()

# upload post for a specific course, used in CreatePost.js
@post_endpoints.route("/api/<idstudent_profile>/feed_post/<course_id>", methods=["POST"])
def upload(idstudent_profile, course_id):
    if request.method == "POST":

        if (text := request.form["text_content"]) != "":
            pass
        else:
            return jsonify({"message": "Can not have empty text content"})

        file_keys = []
        if request.files:
            print(
                f"User {idstudent_profile} attached a file with the post for {course_id}"
            )
            for file_to_upload in request.files.getlist("post_files"):
                new_filename = (
                    uuid.uuid4().hex
                    + "."
                    + file_to_upload.filename.rsplit(".", 1)[1].lower()
                )

                if (type := request.form["type"]) != "":
                    s3_key = f"{type.lower()}/{course_id}/{new_filename}"
                    print("s3 upload response: ", s3_client.upload_file(file_obj=file_to_upload, key=s3_key))
                    file_keys.append(s3_key)
                else:
                    return jsonify({"message": "Error: undefined post type"})
        date_sent = datetime.fromisoformat(request.form.get("date_sent").replace("Z", "+00:00"))
        date_sent = date_sent.strftime('%Y-%m-%d %H:%M:%S')

        post_to_upload = post(
            # idposts=post_id,
            idstudent_profile=request.form.get("idstudent_profile"),
            idclass_profile=request.form.get("idclass_profile"),
            date_sent=date_sent,
            text_content=request.form.get("text_content"),
            # upvote=request.form.get("upvote"),
            response_id=request.form.get("response_id"),
        ) 

        db.session.add(post_to_upload)
        db.session.commit()

        for file_key in file_keys:
            uploaded_file = notes_and_more(
                idposts=post_to_upload.idposts,
                idstudent_profile=idstudent_profile,
                idclass_profile=course_id,
                date_poster=date_sent,
                s3_endpoint=file_key,
            )
            db.session.add(uploaded_file)
            db.session.commit()

        response = jsonify({
            "message": "success",
            # "uploaded_post": post_to_upload
        })
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response, 200

# load feed for a user, display posts from all courses they are enrolled in
@post_endpoints.route("/api/feed/<user_id>/<course_id>", methods=["GET"])
@post_endpoints.route("/api/feed/<user_id>", defaults={'course_id': None}, methods=["GET"])
def feed(user_id, course_id):

    courses = []
    if course_id:
        courses = [course_id]
    else:
        courses = schedule.get_courses_by_student_id(user_id)
        courses = [ course.idclass_profile for course in courses ]

    post_list = post.get_posts_by_class_id_ordered_most_recent(courses)
    posts = create_posts(post_list)
    
    response = jsonify(posts)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200



def create_posts(posts):

    data = []
    for post in posts:
    
        poster_profile = student_profile.get_student_by_id(post.idstudent_profile)
        course = class_profile.get_class_by_id(post.idclass_profile)
        data.append({"id": post.idposts,
            "poster": {"first": poster_profile.f_name, "last": poster_profile.l_name},
            "course": {"name": course.class_name, "code": course.course_code},
            "pfp": "",
            "created": post.date_sent,
            "post_text": post.text_content
        })

    return data