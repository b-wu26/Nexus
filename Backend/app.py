from flask import Flask
from flask_mail import Mail 
from flask_cors import CORS, cross_origin

mail = Mail()

def create_app(): 
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:3000"])

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:SWAGfc%^&*1234@localhost/nexus"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "bananapants"
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'contact.nexuscustomerservice@gmail.com'
    app.config['MAIL_PASSWORD'] = 'mfqhszaedigbcrmb'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    from endpoints.schedule_endpoints import schedule_endpoints
    from endpoints.post_endpoints import post_endpoints
    from endpoints.auth_endpoints import auth_endpoints
    from endpoints.comments_endpoints import comments_endpoints
    from endpoints.courses_endpoints import courses_endpoints

    app.register_blueprint(schedule_endpoints)
    app.register_blueprint(post_endpoints)
    app.register_blueprint(auth_endpoints)
    app.register_blueprint(comments_endpoints)
    app.register_blueprint(courses_endpoints)

    mail.init_app(app)

    return app 
