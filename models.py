

##a file that contains models for the user class and all the forms

#creating the user class
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm #for creating forms through flask
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, RadioField #for creating fields in input forms
from wtforms.validators import InputRequired, Length, ValidationError #for validating user input in the forms
from flask_login import UserMixin

app = Flask(__name__)
db = SQLAlchemy(app)

class Users(db.Model, UserMixin):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("name", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(100), nullable=False)



#creating the registration form
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "password"})
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "confirm_password"})
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

    