from . import db


class student_profile(db.Model):
    idstudent_profile = db.Column(db.Integer, primary_key=True)
    waterloo_id = db.Column(db.String(50), nullable=False,unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    account_password = db.Column(db.String(255))
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    validated = db.Column(db.Boolean)
    bio = db.Column(db.String(50), nullable=True)
    term = db.Column(db.String(50), nullable=True)
    major = db.Column(db.String(50), nullable=True)
    profile_pic = db.Column(db.String(2000), nullable=True)

    def __repr__(self):
        return f"<student_profile {self.f_name}>"

    def __init__(
        self,
        waterloo_id,
        email,
        account_password,
        f_name,
        l_name,
        validated,
    ):
        self.waterloo_id = waterloo_id
        self.account_password = account_password
        self.email = email
        self.f_name = f_name
        self.l_name = l_name
        self.validated = validated

    def get_student_by_id(idstudent_profile):
        return student_profile.query.filter_by(idstudent_profile=idstudent_profile).first()