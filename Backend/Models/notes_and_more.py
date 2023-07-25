from . import db


class notes_and_more(db.Model):
    objectid = db.Column(
        db.Integer, primary_key=True
    )
    idstudent_profile = db.Column(
        db.Integer, db.ForeignKey("student_profile.idstudent_profile"), nullable=False
    )
    idclass_profile = db.Column(
        db.Integer, db.ForeignKey("class_profile.idclass_profile"), nullable=False
    )
    date_poster = db.Column(db.DateTime, nullable=False)
    s3_endpoint = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return f"<notes_and_more {self.objectid}>"

    def __init__(
        self, idstudent_profile, idclass_profile, date_poster, s3_endpoint
    ):
        self.idstudent_profile = idstudent_profile
        self.idclass_profile = idclass_profile
        self.date_poster = date_poster
        self.s3_endpoint = s3_endpoint