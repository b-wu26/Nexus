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

from client.s3_client import S3Client
from models import db

from flask import Flask
from flask_cors import CORS, cross_origin

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

app.register_blueprint(schedule_endpoints)
app.register_blueprint(post_endpoints)
app.register_blueprint(auth_endpoints)

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
                "prof": sch.prof,
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
