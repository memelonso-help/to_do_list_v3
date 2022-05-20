from flask import render_template, Blueprint, flash, session

main = Blueprint("main", __name__, template_folder = "templates")

# you wanna be adding in values into home
@main.route("/")
@main.route("/home")
def home():
    user = None
    if "user" in session:
        user = session["user"]
        flash(f"Hi {user}!")
    else:
        flash("You wanna log in?")
    return render_template("to_do_list_home.html", user = user)