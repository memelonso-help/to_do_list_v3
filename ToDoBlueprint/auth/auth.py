# here you wanna include flask code for signup, login and logout

from collections import UserList
from time import strftime
from flask import render_template, url_for, Blueprint, flash, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash

from ToDoBlueprint.models import userlist, db, login_manager
from flask_login import login_required, login_user, logout_user, fresh_login_required
from ToDoBlueprint.forms import signupform, loginform, changepasswordform

auth = Blueprint("auth", __name__, template_folder = "templates")

# add a signup page
@auth.route("/signup", methods = ["POST", "GET"])
def signup():
    form = signupform(request.form)
    signup_message = None
    if request.method == "POST" and form.validate_on_submit():
        print("a")
        a = userlist.query.filter_by(_user = form.username.data).first()
        if a:
            signup_message = f"Username \"{form.username.data}\" already exists!"
        else:
            new_user = userlist(user = form.username.data, password = generate_password_hash(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            signup_message = f"Hi, account for \"{form.username.data}\" has been created!"
    else:
        flash("Would you like to signup?")
    return render_template("to_do_list_signup.html", signup_message = signup_message, form = form)

@login_manager.user_loader
def load_user(user_id):
    return userlist.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return "User is not authorized for this page."

# add a login page for whoever wanna use the auth
@auth.route("/login", methods = ["POST", "GET"])
def login():
    login_message = None
    form = loginform(request.form)
    logged_in = None
    if request.method == "POST" and form.validate_on_submit():
        a = userlist.query.filter_by(_user = form.username.data).first()
        if a and check_password_hash(a._password, form.password.data):
            logged_in = True
            login_user(a, remember = form.remember.data)
            login_message = f"Welcome {form.username.data}!"
        elif a and not check_password_hash(a._password, form.password.data):
            login_message = "Wrong password."
        else:
            login_message = "No such user exists."
    return render_template("to_do_list_login.html", login_message = login_message, form = form, logged_in = logged_in)

login_manager.refresh_view = "auth.login"

# allow user to change account settings, two forms, one to submit
@auth.route("/settings", methods = ["POST", "GET"])
@fresh_login_required
def change_settings():
    change_message = None
    form = changepasswordform(request.form)
    if request.method == "POST" and form.validate_on_submit():
        a = userlist.query.filter_by(_user = form.username.data).first()
        if a and session["_user_id"] == str(a.id):
            if not check_password_hash(a._password, form.old_password.data):
                change_message = "You have input the wrong original password bro."
            elif form.new_password1.data != form.new_password2.data:
                change_message = "The two new passwords don't match."
            elif check_password_hash(a._password, form.new_password1.data):
                change_message = "Don't reuse your old password man."
            elif form.new_password1.data == form.new_password2.data and check_password_hash(a._password, form.old_password.data):
                a._password = generate_password_hash(form.new_password1.data)
                db.session.commit()
                change_message = "Updated to new password."
            return render_template("to_do_list_settings.html", change_message = change_message, form = form)
        change_message = f"No such user \"{form.username.data}\" found."
    return render_template("to_do_list_settings.html", change_message = change_message, form = form)

@auth.route("/logout")
@login_required
def loqout():
    logout_user()
    return redirect(url_for("auth.login"))