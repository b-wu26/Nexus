import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
#format: dialect+driver://username:password@host:port/database (dialect = mysql for us, driver optional)
#eventually if we have our ec2 up we would need to populate info with above format using whatever RDS creds.

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:your-password@DESKTOP-OETCQGC:3306/nexus'
app.config['SQLALCHEMy_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class student_profile(db.Model):
    idstudent_profile = db.Column(db.Integer, primary_key=True)
    waterloo_id = db.Column(db.String(50), nullable=False)
    account_passwrod = db.Column(db.String(50))
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    validated = db.Column(db.Boolean)

    def __repr__(self):
        return f'<student_profile {self.firstname}>'

@app.route('/')
def index():
    student_profile = student_profile.query.all()
    return render_template('index.html', student_profile=student_profile)
# db.create_all()
# @app.route('/')
# def home():
#     return "hello world"
# if __name__ == "__main__":
#     app.run(debug=True)