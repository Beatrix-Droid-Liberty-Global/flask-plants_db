from flask import Flask, render_template, request, flash, redirect, url_for
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route('/log', methods=["POST", "GET"])
def log():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        return  redirect(url_for('view_plants'))

    return render_template("index.html")


@app.route('/new_user', methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        confirm_username = request.form['new_username']
        new_password = request.form['new_password']
        confirm_password =request.form["confirm_password"]
        return  redirect(url_for('log'))

    return render_template("new_user.html")


@app.route('/view_plants', methods=["POST"])
def view_plants():
    return render_template("your_plants.html")




if __name__ == "__app__":
    app.run(debug=True)