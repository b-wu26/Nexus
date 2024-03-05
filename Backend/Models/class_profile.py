from . import db


class class_profile(db.Model):
    idclass_profile = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(200), nullable=False)
    course_code = db.Column(db.String(30), nullable=False, unique=True)
    faculty = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        return f"<class_profile {self.course_code}>"

    def __init__(self, idclass_profile, class_name, course_code, faculty, description):
        self.idclass_profile = idclass_profile
        self.class_name = class_name
        self.course_code = course_code
        self.faculty = faculty
        self.description = description
        
    def as_dict(self): 
        return {
            "idclass_profile": self.idclass_profile,
            "class_name": self.class_name,
            "course_code": self.course_code,
            "faculty": self.faculty,
            "description": self.description
        }
    
    def get_class_by_id(idclass_profile):
        return class_profile.query.filter_by(idclass_profile=idclass_profile).first()
