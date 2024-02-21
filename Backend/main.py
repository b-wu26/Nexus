import uuid
from datetime import datetime


from flask import request, jsonify, Flask, render_template, session, redirect, url_for

from flask_socketio import SocketIO, send, join_room, leave_room

from flask_mail import Mail, Message 

from models.student_profile import student_profile
from models.class_profile import class_profile
from models.message import message as dbmessage
from models.post import post
from models.schedule import schedule

from client.s3_client import S3Client
from models import db

from posts_helper import create_posts

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/nexus"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "bananapants"
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'contact.nexuscustomerservice@gmail.com'
app.config['MAIL_PASSWORD'] = 'mfqhszaedigbcrmb'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db.init_app(app=app)
mail = Mail(app)


socketio = SocketIO(app)
s3_client = S3Client()

chat_rooms = {}


@app.route("/api/new_user", methods=["POST"])
def new_user():
    if request.method == "POST":
        try:
            new_user = student_profile(
                idstudent_profile=eval(request.form["idstudent_profile"]),
                waterloo_id=request.form["waterloo_id"],
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


@app.route("/api/<idstudent_profile>/feed_post/<course_id>", methods=["POST"])
def upload(idstudent_profile, course_id):
    if request.method == "POST":
        # post_id = uuid.uuid4().hex

        if (text := request.form["text_content"]) != "":
            pass
        else:
            return jsonify({"message": "Can not have empty text content"})

        file_key = None
        if request.files:
            print(
                f"User {idstudent_profile} attached a file with the post for {course_id}"
            )
            file_to_upload = request.files["upload_file"]
            new_filename = (
                uuid.uuid4().hex
                + "."
                + file_to_upload.filename.rsplit(".", 1)[1].lower()
            )

            if (type := request.form["type"]) != "":
                file_key = f"{type.lower()}/{course_id}/{new_filename}"
                print(s3_client.upload_file(file_obj=file_to_upload, key=file_key))
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

        response = jsonify({
            "message": "success",
            # "uploaded_post": post_to_upload
        })
        response.headers.add('Access-Control-Allow-Origin', '*')

        return response, 200

# load feed for a user, display posts from all courses they are enrolled in
@app.route("/api/feed/<user_id>", methods=["GET"])
def feed(user_id):
    courses = schedule.get_courses_by_student_id(user_id)
    courses = [ course.idclass_profile for course in courses ]

    post_list = post.get_posts_by_class_id_ordered_most_recent(courses)
    posts = create_posts(post_list)
    
    response = jsonify(posts)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route("/api/enrolled_courses/<user_id>", methods=["GET"])
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

@app.route("/chat", methods=["POST", "GET"])
def chat(): 
    session.clear()
    if request.method == "POST": 
        username = request.form.get("username")
        password = request.form.get("password") 
        course = request.form.get("course") 
        
        #bunch of error checking
        if not username: 
            return render_template("chat_home.html", error="Please enter a username.")

        if not password: 
            return render_template("chat_home.html", error="Please enter a password.")
        
        if not course: 
            return render_template("chat_home.html", error="Please select a course.")

        user_info = db.session.query(student_profile).filter_by(waterloo_id=username).first()
        course_info = db.session.query(class_profile).filter_by(course_code=course).first() 

        if user_info is None or user_info.account_password != password: 
            return render_template("chat_home.html", error="The username or password is incorrect.")
        
        #valid user, connect to room 
        room = course 
        if room not in chat_rooms: 
            messageList = dbmessage.query.join(student_profile, dbmessage.idstudent_profile == student_profile.idstudent_profile).add_columns(student_profile.waterloo_id, dbmessage.message, dbmessage.idclass_profile).filter(dbmessage.idclass_profile == course_info.idclass_profile).all()
            oldMessages = [] 
            for message in messageList:
                oldMessages.append({
                    "username": message[1],
                    "message": message[2]
                })
            chat_rooms[room] = {"members": 0, "messages": oldMessages} 
            print(chat_rooms)

        session["room"] = room 
        session["username"] = username
        session["user_id"] = user_info.idstudent_profile
        session["course_id"] = course_info.idclass_profile
        return redirect(url_for("room"))

    return render_template("chat_home.html", error="")

@app.route("/room") 
def room(): 

    room = session.get("room")
    if room is None or session.get("username") is None or room not in chat_rooms:
       return redirect(url_for("chat"))
    
    return render_template("chat_room.html", course=room, messages=chat_rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    user_id = session.get("user_id")
    course_id = session.get("course_id")
    if room not in chat_rooms:
        return 
    
    content = {
        "username": session.get("username"),
        "message": data["data"]
    }
    send(content, to=room)
    chat_rooms[room]["messages"].append(content)

    new_message = dbmessage(
        idstudent_profile = user_id,
        idclass_profile = course_id,
        message = data["data"] 
    )   

    db.session.add(new_message)
    db.session.commit()

    print(f"{session.get('username')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    username = session.get("username")
    if not room or not username:
        print("here")
        return
    if room not in chat_rooms:
        messageList = dbmessage.query.join(student_profile, dbmessage.idstudent_profile == student_profile.idstudent_profile).add_columns(student_profile.waterloo_id, dbmessage.message, dbmessage.idclass_profile).filter(dbmessage.idclass_profile == session["course_id"]).all()
        oldMessages = [] 
        for message in messageList:
            oldMessages.append({
                "username": message[1],
                "message": message[2]
            })
        chat_rooms[room] = {"members": 0, "messages": oldMessages} 
    
    join_room(room)
    send({"username": username, "message": "has entered the room"}, to=room)
    chat_rooms[room]["members"] += 1
    print(f"{username} joined room {room}")

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
