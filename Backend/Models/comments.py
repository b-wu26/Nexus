from . import db
from datetime import datetime
from .student_profile import student_profile

class comments(db.Model):
    idcomments = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(2000), nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)
    idstudent_profile = db.Column(db.Integer, db.ForeignKey('student_profile.idstudent_profile'), nullable=False)
    idposts = db.Column(db.Integer, db.ForeignKey('post.idposts'), nullable=False)

    def __repr__(self):
        return f"Comment(id={self.idcomments}, comment='{self.comment}', date_sent='{self.date_sent}', idstudent_profile={self.idstudent_profile}, idposts={self.idposts})"
    

    def __init__(self, comment, idstudent_profile, idposts, date_sent=datetime.utcnow()):
        self.comment = comment
        self.idstudent_profile = idstudent_profile
        self.idposts = idposts
        self.date_sent = date_sent
    
    def get_comments_by_post_id_sorted_and_join_student_profile(post_id):
        return db.session.query(comments, student_profile).filter(comments.idposts==post_id).join(student_profile).order_by(comments.date_sent.asc()).all()
    
    def to_dict(self):
        return {
            'id': self.idcomments,
            'comment': self.comment,
            'date_sent': self.date_sent.isoformat(),
            'idstudent_profile': self.idstudent_profile,
            'idposts': self.idposts
        }