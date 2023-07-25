import uuid

from flask import request, jsonify, Flask, render_template, session, redirect, url_for

from flask_socketio import SocketIO, send, join_room, leave_room

from models.student_profile import student_profile
from models.class_profile import class_profile
from client.s3_client import S3Client
from models import db

from models.student_profile import student_profile
from models.schedule import schedule

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/nexus"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "bananapants"
db.init_app(app=app)

socketio = SocketIO(app)

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


@app.route("/api/<user_id>/feed_post/<course_id>", methods=["POST"])
def upload(user_id, course_id):
    if request.method == "POST":
        post_id = uuid.uuid4().hex

        # TODO: where to store text content
        if (text := request.form["text_content"]) != "":
            pass
        else:
            return jsonify({"message": "Can not have empty text content"})

        file_key = None
        if request.files:
            print(f"User {user_id} attached a file with the post for {course_id}")
            file_to_upload = request.files["upload_file"]
            new_filename = (
                uuid.uuid4().hex
                + "."
                + file_to_upload.filename.rsplit(".", 1)[1].lower()
            )

            if (type := request.form["type"]) != "":
                file_key = f"{type.lower()}/{course_id}/{new_filename}"
                # s3_client.upload_file(file_obj=file_to_upload, key=file_key)
            else:
                return jsonify({"message": "Error: undefined post type"})

        # TODO: put posting info in database

        response = {
            "message": "success",
            "user_id": user_id,
            "post_id": post_id,
            "course_id": course_id,
            "file_key": file_key,
        }

        return jsonify(response)


@app.route("/api/feed/<user_id>", methods=["GET"])
def feed(user_id):
    # TODO: get list of all courses that this person is taking

    # TODO: get top X posts from each course

    # TODO: compile them into lists of posts with data that client(frontend) can use to generate feed

    pass


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

        if user_info is None or user_info.account_password != password: 
            return render_template("chat_home.html", error="The username or password is incorrect.")
        
        #valid user, connect to room 
        room = course 
        if room not in chat_rooms: 
            chat_rooms[room] = {"members": 0, "messages": []} 

        session["room"] = room 
        session["username"] = username
        return redirect(url_for("room"))

    return render_template("chat_home.html", error="")

@app.route("/room") 
def room(): 

    room = session.get("room")
    if room is None or session.get("username") is None or room not in chat_rooms:
       return redirect(url_for("chat"))
    
    return render_template("chat_room.html", course=room)

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in chat_rooms:
        return 
    
    content = {
        "username": session.get("username"),
        "message": data["data"]
    }
    send(content, to=room)
    chat_rooms[room]["messages"].append(content)
    print(f"{session.get('username')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    username = session.get("username")
    if not room or not username:
        return
    if room not in chat_rooms:
        leave_room(room)
        return
    
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
