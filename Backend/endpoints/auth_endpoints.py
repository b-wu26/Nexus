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

auth_endpoints = Blueprint("auth_endpoints", __name__)
s3_client = S3Client()

@auth_endpoints.route("/api/user/login", methods=["POST"])
def login(): 
    if request.method == "POST":        
        email = request.form.get("email")
        password = request.form.get("password")
        user = student_profile.query.filter_by(waterloo_id=email).first()
        if user:
            if user.account_password == password:
                #return with success code 200 
                return jsonify({
                    "message": "Login successful", 
                    "user" : {
                        "waterloo_id" : user.waterloo_id,
                        "first_name" : user.f_name,
                        "last_name" : user.l_name,
                        "idstudent_profile" : user.idstudent_profile,
                    }}), 200 
            else:
                return jsonify({"message": "Incorrect password"}), 401 
        else:
            return jsonify({"message": "User does not exist"}), 401