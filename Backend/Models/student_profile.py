from . import db


class student_profile(db.Model):
    idstudent_profile = db.Column(db.Integer, primary_key=True)
    waterloo_id = db.Column(db.String(50), nullable=False,unique=True)
    account_password = db.Column(db.String(50))
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    validated = db.Column(db.Boolean)

    def __repr__(self):
        return f"<student_profile {self.f_name}>"

    def __init__(
        self,
        idstudent_profile,
        waterloo_id,
        account_password,
        f_name,
        l_name,
        validated,
    ):
        self.idstudent_profile = idstudent_profile
        self.waterloo_id = waterloo_id
        self.account_password = account_password
        self.f_name = f_name
        self.l_name = l_name
        self.validated = validated
