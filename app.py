from flask import Flask, request, jsonify, make_response, current_app
from datetime import timedelta
from functools import update_wrapper
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from flask.ext.cors import CORS
from os.path import join, dirname
from dotenv import load_dotenv
from collections import OrderedDict
from psycopg2.extensions import adapt, register_adapter, AsIs

import flask.ext.restless
import os
import json, ast
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
    search = db.Column(db.String(200))
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

# db.create_all()
# db.session.commit()

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, methods=['GET'])
manager.create_api(Bookmark, methods=['GET'])

users = User.query.all()
bookmarks = Bookmark.query.all()

@app.route("/")
def hello():
    return "Hello World"

@app.route("/add_bookmark", methods=['POST'])
def add_bookmark():

    form_data = json.dumps(request.json)

    middle_data = json.loads(form_data)

    loop_data = ast.literal_eval(json.dumps(middle_data))

    print type(form_data)
    print type(middle_data)
    # print type(almost_data)
    print type(loop_data)
    print form_data
    print middle_data
    # print almost_data
    print loop_data

    user_id_value = str(loop_data['user_id'])
    title_value = str(loop_data['title'])
    notes_value = str(loop_data['notes'])
    search_value = str(loop_data['search'])



    # for key, elem in loop_data.items():
    #     if key == 'user_id':
    #         global user_id_value
    #         print key
    #         user_id_value = adapt(elem).getquoted()
    #     elif key == 'title':
    #         global title_value
    #         print key
    #         title_value = adapt(elem).getquoted()
    #     elif key == 'notes':
    #         global notes_value
    #         print key
    #         notes_value = adapt(elem).getquoted()
    #     elif key == 'search':
    #         global search_value
    #         print key
    #         search_value = adapt(elem).getquoted()
    #     else:
    #         print "didn't work"

    print user_id_value
    print title_value
    print notes_value
    print search_value

    new_bookmark = Bookmark(search_value, "now", notes_value, title_value, user_id_value)
    db.session.add(new_bookmark)
    db.session.commit()

    print "Bookmark added"
    return jsonify(result={"status": 200})

if __name__ == "__main__":
    app.run()
