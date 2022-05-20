# you will be defining consumer related code here, such as the userpage, todolist and completed task list
import os

from flask import render_template, url_for, Blueprint, flash, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

from ToDoBlueprint.models import todolist, donelist, db

consumer = Blueprint("consumer", __name__, template_folder = "templates")

consumer.secret_key = "mommy help" # server interprets each session in an encrypted manner, and secret key is required to decrypt it

def adj_checkbox(which_db, adj_data):
    if which_db == "to_do_list":
        todolist.query.filter_by(task = adj_data).delete()
    donelist.query.filter_by(task = adj_data).delete()
    db.session.commit()

# allow user to fill in to do list here, can view to do list here too
@consumer.route("/user-addtasks", methods = ["POST", "GET"])
def user():
    if "user" in session:
        user = session["user"]
        tasklist = None
        if request.method == "POST" and request.form["to_do_task"] != "":
            task = request.form["to_do_task"]
            duedate = request.form["due_date"]
            priority = request.form["priority"]
            details = request.form["details"]

            tasklist = todolist(user, task, priority, details, duedate)
            db.session.add(tasklist)
            db.session.commit()

        return render_template("to_do_list_user.html", user = user, tasklist = tasklist)
    return redirect(url_for("auth.login"))

@consumer.route("/tasklist", methods = ["POST", "GET"])
def tasklist():
    completed = None
    delete = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            # i want to set it up so that whatever is selected is sent to completed tasks
            completed = request.form.getlist("complete_checkbox")
            delete = request.form.getlist("delete_checkbox")
            for i in completed:
                adj_checkbox("to_do_list", i)
                complist = donelist(user = user, task = i)
                print(complist.task)
                db.session.add(complist)
                db.session.commit()
            for i in delete:
                adj_checkbox("to_do_list", i)
            completed= "".join(i + ", " for i in completed)
            delete= "".join(i + ", " for i in delete)
        return render_template("to_do_list_tasklist.html", task_list = todolist.query.filter_by(_user = user).order_by(todolist.priority.asc(), todolist._id.asc()).all(), completed = completed, delete = delete)
    return redirect(url_for("auth.login"))

# allow user to view completed tasks page
@consumer.route("/completed_tasks", methods = ["POST", "GET"])
def completed_tasks():
    delete = None
    print("a")
    if "user" in session:
        user = session["user"]
        print(user)
        if request.method == "POST":
            # i want to set it up so that whatever is selected is sent to completed tasks
            delete = request.form.getlist("delete_checkbox")
            for i in delete:
                print(delete)
            for i in delete:
                adj_checkbox("comp_list", i)
            delete= "".join(i + ", " for i in delete)
        return render_template("to_do_list_completed_tasks.html", completed = donelist.query.filter_by(_user = user).all(), delete = delete)
    return redirect(url_for("auth.login"))