from . import db


class post(db.Model):
    idposts = db.Column(
        db.Integer, primary_key=True
    )
    idstudent_profile = db.Column(
        db.Integer, db.ForeignKey("student_profile.idstudent_profile"), nullable=False
    )
    idclass_profile = db.Column(
        db.Integer, db.ForeignKey("class_profile.idclass_profile"), nullable=False
    )
    date_sent = db.Column(db.DateTime, nullable=False)
    upvote = db.Column(db.Integer, nullable=False)
    text_content = db.Column(db.String(2000), nullable=False)
    response_id = db.Column(db.Integer,nullable=True)

    def __repr__(self):
        return f"<post {self.idposts}>"

    def __init__(
        self, idstudent_profile, idclass_profile, date_sent, text_content,response_id =-1
    ):
        self.idstudent_profile = idstudent_profile
        self.idclass_profile = idclass_profile
        self.date_sent = date_sent
        self.text_content = text_content
        self.upvote = 0
        self.response_id = response_id

    
    def get_posts_by_class_id(idclass_profile):
        return post.query.filter_by(idclass_profile=idclass_profile).all()
    
    def get_posts_by_class_id_ordered_most_recent(idclass_profile_list):
        return post.query.filter(post.idclass_profile.in_(idclass_profile_list)).order_by(post.date_sent.desc()).all()
    
    def get_post_by_id(idposts):
        return post.query.filter_by(idposts=idposts).first()