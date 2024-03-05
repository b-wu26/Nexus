from flask import Blueprint, request, jsonify
from models.class_profile import class_profile
from client.s3_client import S3Client

courses_endpoints = Blueprint("courses_endpoints", __name__)
s3_client = S3Client()

@courses_endpoints.route("/api/search_courses", methods=["POST"])
def search():
    if request.method == "POST":
        course_name = request.form.get("course_name")
        course_level = request.form.get("course_level")
        faculty = request.form.get("faculty")
        
        print(course_level, course_name, faculty)
        courses = class_profile.query.filter(class_profile.course_code.startswith(course_level)).filter(class_profile.faculty == faculty).all()
        if courses:
            return [course.as_dict() for course in courses], 200
        else:
            return jsonify({"message": "No courses found."}), 404
    else:
        return jsonify({"message": "Invalid request."}), 400 