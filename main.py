##main fiule that contains the flask application

from flask import render_template, url_for, flash, request, redirect #for the functioning of the flask application
from flask_sqlalchemy  import SQLAlchemy #for creating the database
from flask_login import login_user, LoginManager, login_required, logout_user#for logging users in and out

from werkzeug.utils import secure_filename #to ensure that users don't upload an file with a potentially dangerous name (sql injections)
from flask_bcrypt import Bcrypt #for hashing passwords
from config import SECRET_KEY
import api_requests #to process the requests from users


#creating the user class
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm #for creating forms through flask
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, RadioField #for creating fields in input forms
from wtforms.validators import InputRequired, Length, ValidationError #for validating user input in the forms
from flask_login import UserMixin

app = Flask(__name__)

#app configurations
app.config["SECRET_KEY"]= SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 100*1024*1024 #100MB max-limit per image
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///Users.db'

bcrypt = Bcrypt(app)
db= SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)#will allow flask and login manager to work together when users are logging in
login_manager.login_view ="login"




class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)



#creating the registration form
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "password"})
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "confirm password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = Users.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please pick another one.")


#creating the login form
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "password"})
    submit = SubmitField("Login")


#creating the upload image form
class UploadImage(FlaskForm):
    file = FileField(validators=[FileRequired(), FileAllowed(['png', 'jpeg','jpg'], 'Images only!')]) #allow only files with the correct extension to be submitted
    organs = RadioField('Label', choices=[('leaf','leaf'),('flower','flower'),('fruit','fruit'),('bark','bark/stem')])
    upload = SubmitField("Upload")







@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id) # loads the user object from the user id stored in the session



@app.route("/new_user", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.confirm_password.data != form.password.data:
                flash("the two password fields don/t match, please enter them correctly")
                return render_template('new_user.html', form = form)
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = Users(username=form.username.data, password= hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        #insert something here
        flash("Username already exists, please pick another one")
    return render_template("new_user.html", form=form)


@app.route("/log", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #check if user is in db
        user = Users.query.filter_by(username =form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for("view_plants"))
        flash("Username or password entered incorrectly. Please try entering them again.")

    return render_template("index.html", form=form)

@app.route("/view_plants", methods =["GET","POST"])
@login_required
def view_plants():
    #check if the file  the client wants to upload matches the specified requirements
    form = UploadImage()
    if form.validate_on_submit():

        filename = secure_filename(form.file.data.filename)
        form.file.data.save('static/user_uploads/' + filename) #grab the file and save it in the uploads directory


        return render_template("your_plants.html", form = form)
    return render_template("your_plants.html", form = form)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


db.create_all()
if __name__ == "__main__":

    app.run(debug=True)
