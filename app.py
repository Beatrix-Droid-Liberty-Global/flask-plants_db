from flask import Flask, render_template, url_for, flash, request, redirect
from flask_sqlalchemy  import SQLAlchemy
from config import *
from flask_login import UserMixin, login_user, LoginManager, login_required, login_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SECRET_KEY"]="49132rh9ehfr2eh234"
bcrypt = Bcrypt(app)
db= SQLAlchemy(app)
login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view ="login"


class Users(db.Model, UserMixin):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column("name", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(100), nullable=False)


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = Users.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please pick another one.")



class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=100)], render_kw={"placeholder": "password"})
    submit = SubmitField("Login")


db.create_all()

@app.route("/log", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #check if user is in db
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user)
                return redirect(url_for("view_plants"))
        flash("Username or password entered incorrectly. Please try entering them again.")

    return render_template("index.html", form=form)



@app.route("/new_user", methods=["GET", "POST"])
def register_user():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = Users(username=form.username.data, password= hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        #insert something here
        flash("Username already exists, please pick another one")
    return render_template("new_user.html", form=form)


@app.route("/view_plants", methods =["POST"])
@login_required
def view_plants():
    return render_template("your_plants.html")

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == "__app__":
    app.run(debug=True)