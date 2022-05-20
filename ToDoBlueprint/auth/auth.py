# here you wanna include flask code for signup, login and logout

from time import strftime
from flask import render_template, url_for, Blueprint, flash, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash

from ToDoBlueprint.models import userlist, db

auth = Blueprint("auth", __name__, template_folder = "templates")

# add a signup page
@auth.route("/signup", methods = ["POST", "GET"])
def signup():
    signup_message = None
    if request.method == "POST" and request.form["name"] != "" and request.form["password"] != "":
        name = request.form["name"]
        password = request.form["password"]
        a = userlist.query.filter_by(_user = name).first()
        if a:
            signup_message = f"Username \"{name}\" already exists!"
        else:
            new_user = userlist(name, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            signup_message = f"Hi, account for \"{name}\" has been created!"
    else:
        flash("Would you like to signup?")
    return render_template("to_do_list_signup.html", signup_message = signup_message)

# add a login page for whoever wanna use the auth
@auth.route("/login", methods = ["POST", "GET"])
def login():
    login_message = None
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]
        a = userlist.query.filter_by(_user = name).first()
        if a:
            if a._user == name and check_password_hash(a._password, password):
                session["user"] = name
                flash(f"Hi {name}, you have logged in!")
                return redirect(url_for("consumer.user"))
            login_message = "Invalid password!"
        else:
            login_message = "Username does not exist."
    else:
        if "user" in session:
            user = session["user"]
            login_message = f"You have already logged in {user}."
            return redirect(url_for("consumer.user"))
        flash("Login man")
    return render_template("to_do_list_login.html", login_message = login_message)

@auth.route("/logout")
def loqout():
    if "user" in session:
        user = session["user"]
        session.pop("user", None)
        flash(f"{user} has logged out!")
    return redirect(url_for("auth.login"))