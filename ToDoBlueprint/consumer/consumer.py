# you will be defining consumer related code here, such as the userpage, todolist and completed task list
import os

from flask import render_template, url_for, Blueprint, flash, session, request, redirect
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

from ToDoBlueprint.models import todolist, donelist, db
from ToDoBlueprint.forms import taskfillform, tasklistform, complistform

consumer = Blueprint("consumer", __name__, template_folder = "templates")

consumer.secret_key = "mommy help" # server interprets each session in an encrypted manner, and secret key is required to decrypt it

def adj_checkbox(which_db, adj_data):
    if which_db == "to_do_list":
        todolist.query.filter_by(task = adj_data).delete()
    donelist.query.filter_by(task = adj_data).delete()
    db.session.commit()

# allow user to fill in to do list here, can view to do list here too
@consumer.route("/user-addtasks", methods = ["POST", "GET"])
@login_required
def user():
    tasklist = None
    form = taskfillform(request.form)
    if request.method == "POST" and form.validate_on_submit():
        tasklist = todolist(current_user._user, form.task.data, form.priority.data, form.details.data, form.duedate.data)
        db.session.add(tasklist)
        db.session.commit()
    return render_template("to_do_list_user.html", user = current_user._user, form = form)

@consumer.route("/tasklist", methods = ["POST", "GET"])
@login_required
def tasklist():
    completed = None
    delete = None
    form = tasklistform(request.form)
    if request.method == "POST" and form.validate_on_submit():
        # i want to set it up so that whatever is selected is sent to completed tasks
        completed = request.form.getlist("complete_checkbox")
        delete = request.form.getlist("delete_checkbox")
        for i in completed:
            adj_checkbox("to_do_list", i)
            complist = donelist(user = current_user._user, task = i)
            db.session.add(complist)
            db.session.commit()
        for i in delete:
            adj_checkbox("to_do_list", i)
        completed = "".join(i + ", " for i in completed)
        delete = "".join(i + ", " for i in delete)
        form = None
    return render_template("to_do_list_tasklist.html", task_list = todolist.query.filter_by(_user = current_user._user).order_by(todolist.priority.asc(), todolist._id.asc()).all(), completed = completed, delete = delete, form = form)

# allow user to view completed tasks page
@consumer.route("/completed_tasks", methods = ["POST", "GET"])
@login_required
def completed_tasks():
    delete = None
    form = complistform(request.form)
    if request.method == "POST" and form.validate_on_submit():
        delete = request.form.getlist("checkbox")
        for i in delete:
            adj_checkbox("comp_list", i)
            # flash(f"Deleted task {i} from completed list eternally.")
        delete= "".join(i + ", " for i in delete)
    return render_template("to_do_list_completed_tasks.html", completed = donelist.query.filter_by(_user = current_user._user).all(), delete = delete, form = form)