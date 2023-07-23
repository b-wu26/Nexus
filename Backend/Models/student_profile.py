from . import db 

class student_profile(db.Model):
    idstudent_profile = db.Column(db.Integer, primary_key=True)
    waterloo_id = db.Column(db.String(50), nullable=False)
    account_passwrod = db.Column(db.String(50))
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    validated = db.Column(db.Boolean)

    def __repr__(self):
        return f'<student_profile {self.f_name}>'

    def __init__(self, waterloo_id,f_name,l_name):
        waterloo_id = waterloo_id
        f_name = f_name
        l_name = l_name
