from flask import Flask, render_template, request, flash, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
class Users(db.Model, UserMixin):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100), nullable=False, unique=True)
    password = db.Column("password", db.String(100))
    confirm_password = db.Column("confirm_password", db.String(100))

    def __init__(self, name, password, confirm_password=False):
        self.name = name
        self.password = password
        self.confirm_password = confirm_password





@app.route('/log', methods=["POST", "GET"])
def log():
    if request.method == "POST":
        
        username = request.form['username']
        password = request.form['password']
        global found_user
        found_user = Users.query.filter_by(name=username, password=password).first()
    
        if found_user:
            return  redirect(url_for('view_plants'))
        else:
            flash("Username or Password must be incorrect, please check details again")        
    return render_template("index.html")


@app.route('/new_user', methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        confirm_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password =request.form["confirm_password"]
        #check that the new passwords the new user has created exists
        if new_password != confirm_password:
            flash("password input fields don't match, please check again")
            return None

        #check that the username isn't already taken
        if Users.query.filter_by(name=confirm_username).first():
            flash("Username is already taken. Please pick another one to use.")
            return None
        
        #logic to register new user
        usr = Users(confirm_username, new_password, confirm_password)
        db.add(usr)
        db.commit()
        flash("Account succesffuly created, you are being redirected")
        return  redirect(url_for('log'))

    return render_template("new_user.html")

@app.route("/delete user", methods=["POST"])
def delete_user():
    db.delete(found_user)
    db.commit()
    flash("You have successfully deleted the acocount out")
    return redirect(url_for('log'))

@app.route('/view_plants', methods=["POST"])
def view_plants():
    return render_template("your_plants.html")

@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())


if __name__ == "__app__":
    db.create_all()
    app.run(debug=True)