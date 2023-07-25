from . import db
import datetime

class message(db.Model):
    idmessages = db.Column(
        db.Integer, primary_key=True
    )
    idstudent_profile = db.Column(
        db.Integer, db.ForeignKey("student_profile.idstudent_profile"), nullable=False
    )
    idclass_profile = db.Column(
        db.Integer, db.ForeignKey("class_profile.idclass_profile"), nullable=False
    )
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    upvotes = db.Column(db.Integer, nullable=False)
    message = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return f"<message {self.idmessages}>"

    def __init__(
        self, idstudent_profile, idclass_profile, message
    ):
        self.idstudent_profile = idstudent_profile
        self.idclass_profile = idclass_profile
        self.message = message
        self.upvotes = 0