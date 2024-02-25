import uuid

from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db

from models.comments import comments

from client.s3_client import S3Client


s3_client = S3Client()

comments_endpoints = Blueprint("comments_endpoints", __name__)
@comments_endpoints.route("/api/<idstudent_profile>/comment/<idposts>", methods=["POST"])
def upload_comment(idstudent_profile, idposts):
    if request.method == "POST":
        comment = request.form.get("comment")
        date_sent = datetime.fromisoformat(request.form.get("date_sent").replace("Z", "+00:00"))
        date_sent = date_sent.strftime('%Y-%m-%d %H:%M:%S')

        file_keys = []
        if request.files:
            print(
                f"User {idstudent_profile} attached a file with the post for comments"
            )
            for file_to_upload in request.files.getlist("post_files"):
                
                if (type := request.form["type"]) != "":
                    s3_key = f"{type.lower()}/comments/{uuid.uuid4().hex}/{file_to_upload.filename}"
                    print("s3 upload response: ", s3_client.upload_file(file_obj=file_to_upload, key=s3_key))
                    file_keys.append(s3_key)
                else:
                    return jsonify({"message": "Error: undefined post type"})
        print("comment: ", comment)
        comment_to_upload = comments(
            comment=comment,
            idstudent_profile=idstudent_profile,
            idposts=idposts,
            date_sent=date_sent
        )

        db.session.add(comment_to_upload)
        db.session.commit()
        return jsonify({"message": "Comment uploaded successfully"})
    else:
        return jsonify({"message": "Error: Invalid request method"})