##main fiule that contains the flask application

from flask import render_template, url_for, flash, request, redirect #for the functioning of the flask application
from flask_sqlalchemy  import SQLAlchemy #for creating the database
from flask_login import login_user, LoginManager, login_required, logout_user, current_user #for logging users in and out

from werkzeug.utils import secure_filename #to ensure that users don't upload an file with a potentially dangerous name (sql injections)
from flask_bcrypt import Bcrypt #for hashing passwords
from config import SECRET_KEY
from models import app, RegisterForm, LoginForm, Users, UploadImage
import api_requests #to process the requests from users




app.config["SECRET_KEY"]= SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 4*1024*1024 #4MB max-limit per image

bcrypt = Bcrypt(app)
db= SQLAlchemy(app)
login_manager=LoginManager() 
login_manager.init_app(app)#will allow flask and login manager to work together when users are logging in
login_manager.login_view ="login"

@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id) # loads the user object from the user id stored in the session




db.create_all()


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

@app.route("/view_plants", methods =["POST"])
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


if __name__ == "__main__":
    app.run(debug=True)