from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from os.path import join, dirname
from dotenv import load_dotenv
import flask.ext.restless
import os
import json

app = Flask(__name__)
app.config['DEBUG'] = True
# Development
app.config.from_pyfile('config.py')
# #Production
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String())
    nickname = db.Column(db.String())
    email = db.Column(db.String())
    bookmarks = db.relationship('Bookmark', backref='user', lazy='dynamic')

    def __init__(self, social_id, nickname, email):
        self.social_id = social_id
        self.nickname = nickname
        self.email = email

    def __repr__(self):
        return '{}'.format(self.id) + ':' + '{}'.format(self.nickname)

class Bookmark(db.Model):
    __tablename__ = "bookmark"

    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String())
    date_created = db.Column(db.Date())
    notes = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, search, date_created, notes, user_id):
        self.search = search
        self.date_created = date_created
        self.notes = notes
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

db.create_all()
db.session.commit()

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, methods=['GET'])
# manager.create_api(Bookmark, methods)

users = User.query.all()

@app.route("/")
def hello():
    return "Hello World"

@app.route("/get_user", methods=['GET'])
def select():
    return "Hello"

if __name__ == "__main__":
    app.run()
