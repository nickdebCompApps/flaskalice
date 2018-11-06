from aliceinit import app,db
from flask import Flask, render_template, redirect, request
import datetime


from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(UserMixin,db.Model):

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique = True, nullable=False)
    password = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    number = db.Column(db.String(80), unique=True, nullable=False)
    verified = db.Column(db.String(12), nullable = False)
    numberverification = db.Column(db.String(32), nullable=False)
    token = db.Column(db.String(256), nullable=False)
    plan = db.Column(db.String(32), nullable=False)

    date_joined = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    homeworks = db.relationship('Homework', backref='homework', lazy='dynamic')
    messages = db.relationship('Messages', backref='messages', lazy='dynamic')


    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Homework(db.Model):

    __tablename__ = 'Homework'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    duedate = db.Column(db.String(200), nullable = False)
    rawduedate = db.Column(db.String(200), nullable = False)
    homeworktype = db.Column(db.String(200), nullable = False)
    classname = db.Column(db.String(200), nullable = False)
    dateadded = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Homework: {0}, {1}, {2}>'.format(self.classname, self.user_id, self.homeworktype)




class Messages(db.Model):

    __tablename__ = 'Messages'

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key = True)
    message = db.Column(db.String(100), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))


class Subscribers(db.Model):

    __tablename__ = 'Subscribers'

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key = True)
    email = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable=False)
    subscribed = db.Column(db.String(16), nullable=False)
    token = db.Column(db.String(32), nullable=False)
