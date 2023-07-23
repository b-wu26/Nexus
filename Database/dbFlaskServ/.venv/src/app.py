from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:your-password@localhost/nexus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

class student_profile(db.Model):
    idstudent_profile = db.Column(db.Integer, primary_key=True)
    waterloo_id = db.Column(db.String(50), nullable=False)
    account_password = db.Column(db.String(50))
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    validated = db.Column(db.Boolean)
    
    def __repr__(self):
        return f'<student_profile {self.f_name}>'

    def __init__(self,idstudent_profile, waterloo_id,account_password, f_name,l_name, validated):
        self.idstudent_profile = idstudent_profile
        self.waterloo_id = waterloo_id
        self.account_password = account_password
        self.f_name = f_name
        self.l_name = l_name
        self.validated = validated

@app.route('/')
def base():
   return render_template('base.html', student_profiles = student_profile.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['idstudent_profile'] or not request.form['waterloo_id'] or not request.form['account_password'] or not request.form['f_name'] or not request.form['l_name']:
         flash('Please enter all the fields', 'error')
      else:
         print(request)
         print(request.form)
         print(request.form['waterloo_id'])
         new_student_profile = student_profile(request.form['idstudent_profile'], request.form['waterloo_id'],
            request.form['account_password'], request.form['f_name'], request.form['l_name'], True)
         print(new_student_profile.l_name, new_student_profile.f_name)
         db.session.add(new_student_profile)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('base'))
   return render_template('new.html')

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)