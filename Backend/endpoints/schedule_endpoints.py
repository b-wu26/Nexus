from flask import Blueprint, request, jsonify
from models.schedule import schedule
from models.class_profile import class_profile

schedule_endpoints = Blueprint("schedule_endpoints", __name__)

@schedule_endpoints.route("/api/enrolled_courses/<user_id>", methods=["GET"])
def enrolled_courses(user_id):
    if request.method == "GET":
        enrolled_classes = schedule.get_courses_by_student_id(user_id)
        enrolled_courses = [ course.idclass_profile for course in enrolled_classes ]
        response = []
        for course in enrolled_courses:
            class_details = class_profile.get_class_by_id(course)
            response.append({
                "idclass_profile": class_details.idclass_profile,
                "class_name": class_details.class_name,
                "course_code": class_details.course_code,
                "faculty": class_details.faculty
            })
        response = jsonify({"courses": response})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, 200
            