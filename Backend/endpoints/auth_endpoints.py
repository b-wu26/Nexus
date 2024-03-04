import uuid
from datetime import datetime
from models import db

from flask import Blueprint, request, jsonify
from flask_mail import Message
from app import mail

from werkzeug.security import generate_password_hash, check_password_hash

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
        email_or_id = request.form.get("email_or_id")
        password = request.form.get("password")
        user = student_profile.query.filter_by(waterloo_id=email_or_id).first()

        if not user: 
            user = student_profile.query.filter_by(email=email_or_id).first()

        if user:
            if check_password_hash(user.account_password, password):
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
                return jsonify({"message": "Incorrect password.", "error_type": "0"}), 401 
        else:
            return jsonify({"message": "User was not found. Please make sure you entered a valid UWaterloo email or ID.", "error_type": "1"}), 401
        
@auth_endpoints.route("/api/user/signup", methods=["POST"])
def signup(): 
    if request.method == "POST":
        print(request.form)
        user_email = request.form.get("email")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        msg = Message(subject="Confirm your Nexus Account", sender="contact.nexuscustomerservice@gmail.com", recipients=[user_email])
        msg.html = '''<div> <p>Hi there {first_name}, welcome to Nexus! To complete your account signup, please 
        <a href='localhost:3000/login'>click here.</a></p>. 

        <p>Thanks!</p>
        <p>-Nexus Team</p>'''.format(first_name = first_name)
        mail.send(msg)

        new_user = student_profile(
            waterloo_id = request.form["email"].split("@")[0],
            account_password= generate_password_hash(password),
            email=user_email,
            f_name=first_name,
            l_name=last_name,
            validated=True,
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
                    "message": "Email Sent", 
                }), 200 

        
        


