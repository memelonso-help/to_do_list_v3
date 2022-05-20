# in ver 3, start to separate out the pages into blueprint state
# home page can be placed in a general blueprint and templates file, in main.py
# signup, login, logout can be shifted to auth blueprints and template file, in auth.py
# user, tasklist and completed tasklist can be shifted to consumer blueprints and template file, in consumer.py
# set up of env for this app, as well as requirements.txt files
# encrypted(hashed?) the passwords
# update the app functionality to include elaboration column and priority column
# changed elaborate textbox into text area
# update login function using flask_login

from flask import render_template, url_for, Flask, Blueprint, flash, session, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime
from flask_login import LoginManager

from ToDoBlueprint.auth.auth import auth
from ToDoBlueprint.consumer.consumer import consumer
from ToDoBlueprint.general.main import main
from ToDoBlueprint.models import db

def create_app():
    app = Flask(__name__)

    app.secret_key = "mommy help" # server interprets each session in an encrypted manner, and secret key is required to decrypt it
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3" 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

    db.init_app(app)

    app.register_blueprint(main, url_prefix = "")
    app.register_blueprint(auth, url_prefix = "/auth")
    app.register_blueprint(consumer, url_prefix = "/mypages")

    return app

app = create_app()
app.app_context().push()

if __name__ == "__main__":
    # db.drop_all()
    db.create_all()
    app.run(debug = True)