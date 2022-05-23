# changing to sqlalchemy and sqlalchemy.orm packages on next edition
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from datetime import datetime, date
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
login_manager = LoginManager()

class userlist(db.Model, UserMixin):
    __tablename__ = "userlist"

    id = db.Column(db.Integer, primary_key = True)
    _user = db.Column(db.String(20), unique = True)
    _password = db.Column(db.String(200))
    todoass = relationship("todolist", cascade = "all, delete", back_populates = "bossuser")
    compass = relationship("donelist", cascade = "all, delete", back_populates = "bossuser")

    def __init__(self, user, password):
        self._user = user
        self._password = password

    def get(self):
        if self.id in userlist.id:
            return self

class todolist(db.Model):
    __tablename__ = "todolist"

    _id = db.Column(db.Integer, primary_key = True)
    _user = db.Column(db.String(200))
    _userid = db.Column(db.Integer, ForeignKey("userlist.id"))
    task = db.Column(db.String(200))
    due_date = db.Column(db.Date)
    priority = db.Column(db.Integer)
    details = db.Column(db.String(250))
    bossuser = relationship("userlist", back_populates = "todoass")

    def __init__(self, user, task, priority, details, due_date = None):
        self._user = user
        self.task = task
        self.due_date = due_date
        self.priority = priority
        self.details = details

class donelist(db.Model):
    __tablename__ = "donelist"

    _id = db.Column(db.Integer, primary_key = True)
    _user = db.Column(db.String(200))
    _userid = db.Column(db.Integer, ForeignKey("userlist.id"))
    task = db.Column(db.String(200))
    due_date = db.Column(db.String(200)) # might wanna change this to allow for notifications in the future
    completed_date = db.Column(db.Date)
    priority = db.Column(db.Integer)
    details = db.Column(db.String(250))
    bossuser = relationship("userlist", back_populates = "compass")


    def __init__(self, user = None, to_do_list_id = None, task = None,  priority = None, details = None, due_date = None):
        self._user = user
        self.task = task
        self.due_date = due_date
        self.to_do_list_id = to_do_list_id
        self.completed_date = date.today()
        self.priority = priority
        self.details = details
        
