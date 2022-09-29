from flask import Flask, render_template, request, flash, redirect, url_for
from config import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'

app.config['SECRET_KEY'] = 'my-secret-key'


db = SQLAlchemy(app)

class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(100), nullable=False, unique=True)
    
    #password stuff
    password = db.Column("password", db.String(100))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    confirm_password = db.Column("confirm_password", db.String(100))

    def __init__(self, name, password, confirm_password=None):
        self.name = name
        self.password = password
        self.confirm_password = confirm_password



 
db.create_all()
@app.route('/log', methods=["POST", "GET"])
def log():
    if request.method == "POST":
        
        username = request.form['username']
        password = request.form['password']
        global found_user
        found_user = Users.query.filter_by(name=username).first()
    
        if found_user:
            if found_user.password == password:
                return  redirect(url_for('view_plants'))
        else:
            flash("Username or Password must be incorrect, please check details again")  
            return render_template("index.html")
     
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
            return redirect(url_for('register_user'))

        #check that the username isn't already taken
        if Users.query.filter_by(name=confirm_username).first():
            flash("Username is already taken. Please pick another one to use.")
            return redirect(url_for('register_user'))

        
        #logic to register new user
        usr = Users(name=confirm_username, password=new_password, confirm_password=confirm_password)
        db.session.add(usr)
        db.session.commit()
        return  redirect(url_for('log'))

    return render_template("new_user.html")

@app.route("/delete user", methods=["POST"])
def delete_user():
    db.session.delete(found_user)
    db.session.commit()
    flash("You have successfully deleted the acocount out")
    return redirect(url_for('log'))

@app.route('/view_plants', methods=["POST"])
def view_plants():
    return render_template("your_plants.html")

@app.route("/view")
def view():
    return render_template("view.html", values=Users.query.all())


if __name__ == "__app__":
   
    app.run(debug=True)