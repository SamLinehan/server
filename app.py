from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from os.path import join, dirname
from dotenv import load_dotenv
import flask.ext.restless
import os
import json


app = Flask(__name__, instance_relative_config=True)
app.config['DEBUG'] = True
heroku = Heroku(app)
CORS(app)

# Development
app.config.from_pyfile('config.py')
# app.config.from_envvar('DATABASE_URL')
# #Production
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

# @app.route("/add_bookmark", methods=['POST'])
# def add_bookmark():
    # another_bookmark = db.engine.execute("INSERT INTO bookmark VALUES (default, 'now', 'New search 2', 1, 'Yeahh buddy');")

    # data = request.get_data()
    # print data
    # new_data = json.loads(data)
    # print new_data
    # # for key, value in new_data:
    # #     print key + ": " + value


if __name__ == "__main__":
    app.run()
