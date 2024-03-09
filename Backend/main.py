from flask import request, jsonify, Flask, render_template, session, redirect, url_for

from flask_socketio import SocketIO, send, join_room, leave_room

from flask_mail import Mail, Message 

from models.student_profile import student_profile
from models.class_profile import class_profile
from models.message import message as dbmessage
from models.schedule import schedule
from models.post import post
from endpoints.schedule_endpoints import schedule_endpoints
from endpoints.post_endpoints import post_endpoints
from endpoints.auth_endpoints import auth_endpoints
from endpoints.comments_endpoints import comments_endpoints
from datetime import date
from client.s3_client import S3Client
from models import db

from flask import Flask
from flask_cors import CORS, cross_origin
from app import create_app

from datetime import datetime
import timeago

app = create_app() 
db.init_app(app=app)
socketio = SocketIO(app, cors_allowed_origins="*")
s3_client = S3Client()

chat_rooms = {}

@app.route("/api/new_user", methods=["POST"])
def new_user():
    if request.method == "POST":
        try:
            new_user = student_profile(
                idstudent_profile=eval(request.form["idstudent_profile"]),
                waterloo_id=request.form["waterloo_id"],
                email=request.form["email"],
                account_password=request.form["account_password"],
                f_name=request.form["f_name"],
                l_name=request.form["l_name"],
                validated=eval(request.form["validated"]),
            )

            db.session.add(new_user)
            db.session.commit()
            print(f"new user: {request.form['waterloo_id']} was added to Nexus")
            return jsonify({"message": "success"})
        except Exception as e:
            print(f"Failed to create new user: {e}")
            return jsonify({"message": "failed"})


# TODO: add more search parameter for courses, not just by faculty
@app.route("/api/courses", defaults={"faculty": None}, methods=["GET"])
@app.route("/api/courses/<faculty>", methods=["GET"])
def courses(faculty):
    if request.method == "GET":
        courses = class_profile.query.filter_by(faculty=faculty)
        response = []
        for course in courses:
            response.append(
                {
                    "idclass_profile": course.idclass_profile,
                    "class_name": course.class_name,
                    "course_code": course.course_code,
                    "faculty": course.faculty,
                }
            )

        return jsonify({"courses": response})

@app.route("/api/courses/course/<course_id>", methods=["GET"])
def course(course_id):
    if request.method == "GET":
        print(course_id)
        courses = class_profile.query.filter_by(idclass_profile=course_id)
        response = []
        for course in courses:
            lastActive = 'Unknown'
            lastMsg = dbmessage.query.filter_by(idclass_profile = course_id).order_by(dbmessage.date_sent.desc()).first()
            if lastMsg:

                lastActive = timeago.format(lastMsg.date_sent.timestamp(), datetime.now().timestamp())

            response.append(
                {
                    "idclass_profile": course.idclass_profile,
                    "class_name": course.class_name,
                    "course_code": course.course_code,
                    "faculty": course.faculty,
                    "lastActive": str(lastActive)
                }
            )
        print(response)
        return jsonify({"courses": response[0]})

@app.route("/api/user_info/subscribe/<user_id>/<course_id>", methods=["POST", "DELETE", "GET"])
def subscribe(user_id, course_id):
    if request.method == "POST":
        sched = schedule.query.filter_by(idclass_profile=course_id, idstudent_profile=user_id).first()
        if(sched):
            print("This class is already added")
            return jsonify({"response": "this class is already added"})
        today = date.today()
        term = ""
        if(today < date(today.year, 5,1)):
            term = f"Winter_{today.year}"
        elif(today < date(today.year, 9,1)):
            term = f"Spring_{today.year}"
        else:
            term = f"Fall_{today.year}"
        new_scheudle = schedule(
            idstudent_profile=user_id,
            idclass_profile=course_id,
            Term_year=term,
            current_term=True,
        )

        db.session.add(new_scheudle)
        db.session.commit()
        return jsonify({"email": "success"})
    elif request.method == "DELETE":
        sched = schedule.query.filter_by(idclass_profile=course_id, idstudent_profile=user_id).first()
        print(sched)
        message = ""
        if(sched):
            db.session.delete(sched)
            db.session.commit()
            message = "Schedule deleted"
            print(message)
        else:
            message = "There is no schedule to be found"
            print(message)
        return jsonify({"update": message})
    elif request.method == "GET":
        sched = schedule.query.filter_by(idclass_profile=course_id, idstudent_profile=user_id).first()
        if(sched):
            return jsonify({"response": "subscribed"})
        else:
            return jsonify({"response": "not subscribed"})

@app.route("/api/user_info/<user_id>", methods=["PUT", "GET"])
def users(user_id):
    if request.method == "GET":
        user_info = student_profile.get_student_by_id(user_id)
        if user_info is None:
            return("Unlucky")
        user_schedule = db.session.query(schedule, class_profile).select_from(schedule).join(class_profile).filter(schedule.idstudent_profile == user_id, schedule.current_term == 1).all()
        # print(user_info)
        classes = []
        # print(user_schedule)
        for sch, cla in user_schedule:
            classes.append({
                "class_name": cla.class_name,
                "course_code": cla.course_code,
                "faculty": cla.faculty,
                "term": sch.Term_year,
            })

        user_posts = db.session.query(post, class_profile).select_from(post).join(class_profile).filter(post.idstudent_profile == user_id).order_by(post.date_sent).limit(2).all()

        posts = []

        for p, cl in user_posts:
            posts.append({
                "class_name": cl.class_name,
                "text_content": p.text_content,
                "course_code": cl.course_code,
            })
        

        data = {"info":{
            "first": user_info.f_name, 
            "last": user_info.l_name, 
            "waterloo_id": user_info.waterloo_id, 
            "bio": user_info.bio,
            "term": user_info.term,
            "major": user_info.major,
            }, "classes": classes,
            "posts": posts}
        # print(data)
        return data
    elif request.method == "PUT":
        #need to account for editing to login informations
        # print("LFGs")
        # print(request.form.get("bio"))
        # print(request.form.to_dict().keys())
        bio = request.form.get("bio")
        major = request.form.get("major")
        term = request.form.get("term")
        print(type(bio), type(major), type(term))
        user_req_id = request.form.get("idstudent_profile")
        assert user_req_id == user_id
        user_profile = db.session.query(student_profile).filter_by(idstudent_profile = 1).first()
        user_profile.bio = str(bio)
        user_profile.major = str(major)
        user_profile.term = str(term)

        print(user_profile.bio, user_profile.major, user_profile.term)
        db.session.commit()
        print(user_profile)

        user_profile_cehck = db.session.query(student_profile).filter_by(idstudent_profile = 1).first()

        print(user_profile_cehck.bio, user_profile_cehck.major, user_profile_cehck.term)
        return jsonify({"update": "success"}) 

@app.route("/api/<user_id>/signup", methods=["POST"]) 
def signup(user_id): 
    if request.method == "POST": 
        msg = Message(subject="Confirm your Nexus Account", sender="contact.nexuscustomerservice@gmail.com", recipients=[request.form["email"]])
        msg.body = '''Hi there {watid}, welcome to Nexus! To complete your account signup, please click on the below link. 

http://127.0.0.1:5000/verify/{watid}

Thanks!
-Nexus Team'''.format(watid = request.form["watid"])
        mail.send(msg) 

        new_user = student_profile(
            waterloo_id=request.form["watid"],
            account_password=request.form["password"],
            email=request.form["email"],
            f_name=request.form["f_name"],
            l_name=request.form["l_name"],
            validated=True,
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({"email": "success"}) 
   
@app.route("/verify/<watid>") 
def verify(watid): 
    return redirect(url_for("chat"))

@app.route("/chat/<user_id>/<course_id>")
def chat(user_id, course_id):
    classProfile = class_profile.query.filter_by(idclass_profile = course_id).first()
    courseName = classProfile.faculty + ' ' + classProfile.course_code
    
    #valid user, connect to room 
    room = course_id
    if room not in chat_rooms: 
        messageList = dbmessage.query.filter_by(idclass_profile = course_id).order_by(dbmessage.date_sent.asc()).all()
        oldMessages = [] 
        for message in messageList:
            oldMessages.append({
                "username": message.idstudent_profile,
                "message": message.message,
                "date_sent": int(datetime(message.date_sent.year, message.date_sent.month, message.date_sent.day).timestamp())
            })
        chat_rooms[room] = {"members": 0, "messages": oldMessages} 

    session["room"] = room
    session["user_id"] = user_id
    
    return render_template("chat_room.html", course=room, messages=chat_rooms[room]["messages"], user_id=user_id, courseName=courseName)

@socketio.on("join")
def on_join(data):
    room = data["data"]
    join_room(room)
    chat_rooms[room]["members"] += 1

@socketio.on("message")
def message(data):
    room = data["room"]
    user_id = data["user_id"]
    
    if room not in chat_rooms:
        return

    date_sent = datetime.fromtimestamp(data["date_sent"])
    print(date_sent)

    content = {
        "username": user_id,
        "message": data["data"],
        "date_sent": data["date_sent"]
    }
    send(content, to=room)
    chat_rooms[room]["messages"].append(content)

    new_message = dbmessage(
        idstudent_profile = user_id,
        idclass_profile = room,
        message = data["data"],
        date_sent = date_sent
    )   

    db.session.add(new_message)
    db.session.commit()

    print(f"{session.get('username')} said: {data['data']}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    username = session.get("username")
    leave_room(room)

    if room in chat_rooms:
        chat_rooms[room]["members"] -= 1
        if chat_rooms[room]["members"] <= 0:
            del chat_rooms[room]
    
    send({"username": username, "message": "has left the room"}, to=room)
    print(f"{username} has left the room {room}")

@app.route(
    "/api/schedule/<idstudent_profile>",
    methods=["GET"],
)
@app.route(
    "/api/schedule/<idstudent_profile>/<Term_year>",
    methods=["GET"],
)
@app.route(
    "/api/schedule/<idstudent_profile>/<Term_year>/<idclass_profile>/", methods=["GET"]
)
def student_schedule(idstudent_profile, Term_year=None, idclass_profile=None):
    if request.method == "GET":
        filters = {"idstudent_profile": idstudent_profile}

        if idclass_profile is not None:
            filters["idclass_profile"] = idclass_profile

        if Term_year is not None:
            filters["Term_year"] = Term_year

        schedules = schedule.query.filter_by(**filters).all()
        reponse = []
        for s in schedules:
            reponse.append(
                {
                    "idstudent_profile": s.idstudent_profile,
                    "idclass_profile": s.idclass_profile,
                    "Term_year": s.Term_year,
                    "current_term": s.current_term,
                    "prof": s.prof,
                }
            )
        return jsonify({"schedules": reponse})


# @app.route("")
# def


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

if __name__ == "__main__":
    socketio.run(app, debug=True)
