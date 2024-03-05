import uuid
from datetime import datetime
from models import db

from flask import Blueprint, request, jsonify

from models.student_profile import student_profile
from models.class_profile import class_profile
from models.schedule import schedule
from models.post import post
from models.notes_and_more import notes_and_more
from models.comments import comments

from client.s3_client import S3Client

S3_PATH_PREFIX = "https://uw-nexus-contents.s3.us-east-2.amazonaws.com/"
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
                
                if (type := request.form["type"]) != "":
                    s3_key = f"{type.lower()}/{course_id}/{uuid.uuid4().hex}/{file_to_upload.filename}"
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

        attachments = notes_and_more.get_notes_by_post_id(post.idposts)
        # images with s3_endpoint ending with jpeg, jpg, png, or other images files append to images
        images = [f"{S3_PATH_PREFIX}{attachment.s3_endpoint}" for attachment in attachments if attachment.s3_endpoint.lower().endswith(('.jpeg', '.jpg', '.png'))]
        # files with s3_endpoint ending with pdf, docx, or other file types append to files 
        files = [f"{S3_PATH_PREFIX}{attachment.s3_endpoint}" for attachment in attachments if not attachment.s3_endpoint.lower().endswith(('.jpeg', '.jpg', '.png'))]
        
        post_comments = comments.get_comments_by_post_id_sorted_and_join_student_profile(post.idposts)
        
        comment_list = []
        for comment, profile in post_comments:
            comment_attachments = notes_and_more.get_notes_by_comment_id(comment.idcomments)
            comment_images = [f"{S3_PATH_PREFIX}{comment_attachments.s3_endpoint}" for comment_attachments in comment_attachments if comment_attachments.s3_endpoint.lower().endswith(('.jpeg', '.jpg', '.png'))]
            comment_files = [f"{S3_PATH_PREFIX}{comment_attachments.s3_endpoint}" for comment_attachments in comment_attachments if not comment_attachments.s3_endpoint.lower().endswith(('.jpeg', '.jpg', '.png'))]
            
            # print("comment attachments:")
            # print(comment_images, comment_files)
            
            comment_list.append({
                "id": comment.idcomments,
                "comment": comment.comment,
                "date_sent": comment.date_sent.isoformat(),
                "idstudent_profile": profile.idstudent_profile,
                "idposts": comment.idposts,
                "f_name": profile.f_name,
                "l_name": profile.l_name,
                "attachments": {
                    "images": comment_images,
                    "files": comment_files
                }
            })


        poster_profile = student_profile.get_student_by_id(post.idstudent_profile)
        course = class_profile.get_class_by_id(post.idclass_profile)
        data.append({"id": post.idposts,
            "poster": {"first": poster_profile.f_name, "last": poster_profile.l_name},
            # "course": {"id": post.idclass_profile, "name": course.class_name, "code": course.course_code},
            "course": {"id": post.idclass_profile, "name": course.class_name, "code": course.course_code, "faculty": course.faculty},
            "pfp": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAPFBMVEXk5ueutLepsLPo6uursbXJzc/p6+zj5ea2u76orrKvtbi0ubzZ3N3O0dPAxcfg4uPMz9HU19i8wcPDx8qKXtGiAAAFTElEQVR4nO2d3XqzIAyAhUD916L3f6+f1m7tVvtNINFg8x5tZ32fQAIoMcsEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQRAEQTghAJD1jWtnXJPP/54IgNzZQulSmxvTH6oYXX4WS+ivhTbqBa1r26cvCdCu6i0YXbdZ0o4A1rzV+5IcE3YE+z58T45lqo7g1Aa/JY5tgoqQF3qb382x7lNzBLcxft+O17QUYfQI4IIeklKsPSN4i6LKj/7Zm8n99RbHJpEw9gEBXNBpKIYLJqKYRwjOikf//r+J8ZsVuacbqCMNleI9TqGLGqMzhnVdBOdd6F/RlrFijiCoVMk320CBIahUxTWI0KKEcJqKbMdpdJb5QvdHq6wCI5qhKlgGMS/RBHkubWDAE+QZxB4xhCyDiDkLZxgGEVdQldzSKbTIhmZkFkSEPcVvmBn2SMuZB9od7fQDsMiDdKJjFUSCQarM5WirZ3C2TT/htYnyPcPfgrFHWz0BI74gr6J/IZiGUxAZGQLqmvQLTrtE/Go4YxhVRIpEw+sww1IIcqr5NKmUUzLF3d4/qPkYIp2T/obPuemlojFUR4t9Q2Vojhb7BmgElWHzLPH8hucfpefPNFTVgs9h1AdU/Pin96vwWbWdf+X9Absn3OdO34aMdsDnP8WgKYisTqI6CkNGqZQo1XA6Ef6AU32SJzOcBukHPF07/xNSgmHKa5BOhtezv6mA/rYJpwXNAnbRZ1XuF3BzDcO3vpA3+ny2909gbqE4hhD3LIPhLLyBNhPZvbZ3B+3tPYa18A7auSlXQayKwTPNLKDcuOB0xPYKDPFTkWsevQPRZ1J8Hji9I1KQ34r7hZhrwNwOZ97QxNx0drwn4QI0wQk1DcEsfKCWKdxVvxPSNUIp/knmAXT+nT+Ko3+0H96rcNb3m1fx7MBTJdeBJ7uFcWsc0wvgAsC4pROW0l2inbAmIBv/7GZmuhQH6API2rr8T0e6yuZJ+80A9LZeG62T3tik31XwxtwZcizKuTHkMjB1WdZde4Kmic/A5ZI3rr1ae21d08PlVHYfAaxw9G9CYRbJ+8ZdbTcMRV1XM3VdF0M32vtoTdZ0+u29s0OttJ5bz64UwinjaFMVY9vkqc3KKSxN21Xl+0L4Q3Vuv1tYl0pqnX6ms4XetFz7gdZVAgUEoJntfOUe4ZwsHd9FzqQ3Vv6xe41l0XJcqcKl6TZvlv7ClAW3BsqQW4X7ypApB8dmTgK4IX5wvqIVj33HtD2qSG4BqznxdIefL27Y4sahi0MdIdvUsDva8agGGbCtITmCY31MHD2O0uIdh/0rJDQ1VX5Zdxz3rR2QDbv6qXl9vudzqQtGm1Jv9LDXOsfvvB7VcZ8PDKD0mQ1VHPYQ9O+Yj4hR1IUD8rBnn3ho2m8oQMxbCFiKlL2ioSW5heeJqegED52CzxCtcGD3Kv8Wms9EYLyUhwaFIhSMBClevWEmiK/Iaogu4H7sg6ppQhQG8RUqivuTGOAJOg6FfgW0q0M0PQMRMEgXaeNf3SYDZ8PIMI0+wHgr/MgN7wYwpiLjCCqM6ydUDZLQiB6nDdNC8SDyig3jPPpFXGcC9O8BUBDVmgBY59E7Md/35Loe/UVEECEJwYggJjELZ4J71SaQSBeC02n4Da29CayJNA28SAhd2CQyC1Xw6pSmGSINQVuMhAZp4DClan9MgmkDDNmezqwS8sgtlXK/EPBhoaSmYVC/F7IO1jQEdHOlabpKh3+jzLQSTUiq4X2I+Ip/zU8rlaqAvkS21ElR+gqu3zbjjL+hIAiCIAiCIAiCIAiCsCf/AKrfVhSbvA+DAAAAAElFTkSuQmCC",
            "created": post.date_sent,
            "post_text": post.text_content,
            "attachments" : {
                "images" : images,
                "files" : files
            },
            "comments" : comment_list
        })

    return data