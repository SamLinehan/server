from flask import Flask, request, jsonify, make_response, current_app
from datetime import timedelta
from functools import update_wrapper
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from flask.ext.cors import CORS
from os.path import join, dirname
from dotenv import load_dotenv
import flask.ext.restless
import os
import json
import ast


app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = True
heroku = Heroku(app)
CORS(app, resources=r'/*', allow_headers='Content-Type')

app.config.from_pyfile('config.py')
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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


class Bookmark(db.Model):
    __tablename__ = "bookmark"

    id = db.Column(db.Integer, primary_key=True)
    search = db.Column(db.String())
    date = db.Column(db.Date())
    notes = db.Column(db.String())
    title = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, search, date, notes, title, user_id):
        self.search = search
        self.date = date
        self.notes = notes
        self.title = title
        self.user_id = user_id

db.create_all()
db.session.commit()

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, methods=['GET'])
manager.create_api(Bookmark, methods=['GET'])

users = User.query.all()
bookmarks = Bookmark.query.all()

# Testing Insert Statement
# new_bookmark = Bookmark("Chordata", "now", "Testing insert", "Test", 1)
# db.session.add(new_bookmark)
# db.session.commit()

@app.route("/")
def hello():
    return "Hello World"

@app.route("/add_bookmark", methods=['POST'])
def add_bookmark():

    form_data = json.dumps(request.json)

    loop_data = json.loads(form_data)

    print type(form_data)
    print type(loop_data)
    print form_data
    print loop_data

    user_id_value = 0
    title_value = ''
    notes_value = ''
    search_value = ''

    for key, elem in loop_data.items():
        if key is 'user_id':
            print key
            user_id = elem
            print user_id
        elif key is 'title':
            print key
            title = elem
            print title
        elif key is 'notes':
            print key
            notes = elem
            print notes
        elif key is 'search':
            print key
            search_value = elem
            print search
        else:
            print "didn't work"


    new_bookmark = Bookmark(search_value, "now", notes_value, title_value, user_id_value)
    db.session.add(new_bookmark)
    db.session.commit()

    # new_bookmark = Bookmark(search_value, 'now', notes_value, title_value, user_id_value)
    # db.session.add(new_bookmark)

    print "Bookmark added"
    return jsonify(result={"status": 200})

if __name__ == "__main__":
    app.run()
