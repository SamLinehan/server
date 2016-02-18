from flask import Flask, request, jsonify, make_response, current_app
# from flask.ext import restful
# from flask.ext.restful import Api
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


app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = True
heroku = Heroku(app)
CORS(app, resources=r'/*', allow_headers='Content-Type')

# api = restful.Api(app)

app.config.from_pyfile('config.py')
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

db = SQLAlchemy(app)

# CORS Snippet

# def crossdomain(origin=None, methods=None, headers=None,
#                 max_age=21600, attach_to_all=True,
#                 automatic_options=True):
#     if methods is not None:
#         methods = ', '.join(sorted(x.upper() for x in methods))
#     if headers is not None and not isinstance(headers, basestring):
#         headers = ', '.join(x.upper() for x in headers)
#     if not isinstance(origin, basestring):
#         origin = ', '.join(origin)
#     if isinstance(max_age, timedelta):
#         max_age = max_age.total_seconds()
#
#     def get_methods():
#         if methods is not None:
#             return methods
#
#         options_resp = current_app.make_default_options_response()
#         return options_resp.headers['allow']
#
#     def decorator(f):
#         def wrapped_function(*args, **kwargs):
#             if automatic_options and request.method == 'OPTIONS':
#                 resp = current_app.make_default_options_response()
#             else:
#                 resp = make_response(f(*args, **kwargs))
#             if not attach_to_all and request.method != 'OPTIONS':
#                 return resp
#
#             h = resp.headers
#             h['Access-Control-Allow-Origin'] = origin
#             h['Access-Control-Allow-Methods'] = get_methods()
#             h['Access-Control-Max-Age'] = str(max_age)
#             h['Access-Control-Allow-Credentials'] = 'true'
#             h['Access-Control-Allow-Headers'] = \
#                 "Origin, X-Requested-With, Content-Type, Accept, Authorization"
#             if headers is not None:
#                 h['Access-Control-Allow-Headers'] = headers
#             return resp
#
#         f.provide_automatic_options = False
#         return update_wrapper(wrapped_function, f)
#     return decorator

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

    def __init__(self, search, date_created, notes, title, user_id):
        self.search = search
        self.date_created = date_created
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

@app.route("/")
def hello():
    return "Hello World"

@app.route("/add_bookmark", methods=['POST'])
# @crossdomain(origin='https://twig-of-life.herokuapp.com')
def add_bookmark():

    form_data = json.dumps(request.json)

    print form_data

    # another_bookmark = db.engine.execute("INSERT INTO bookmark VALUES (default, 'now', 'New search 2', 1, 'Yeahh buddy');")

    print "Bookmark added"
    return jsonify(result={"status": 200})

if __name__ == "__main__":
    app.run()
