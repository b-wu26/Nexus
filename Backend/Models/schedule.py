from . import db


class schedule(db.Model):
    idstudent_profile = db.Column(
        db.Integer, db.ForeignKey("student_profile.idstudent_profile"), primary_key=True
    )
    idclass_profile = db.Column(
        db.Integer, db.ForeignKey("class_profile.idclass_profile"), primary_key=True
    )
    Term_year = db.Column(db.String(45), primary_key=True)
    current_term = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<schedule {self.idclass_profile}, {self.idclass_profile}, {self.Term_year}>"

    def __init__(
        self, idstudent_profile, idclass_profile, Term_year, current_term
    ):
        self.idstudent_profile = idstudent_profile
        self.idclass_profile = idclass_profile
        self.Term_year = Term_year
        self.current_term = current_term

    def get_courses_by_student_id(idstudent_profile):
        return schedule.query.filter_by(idstudent_profile=idstudent_profile).all()
    