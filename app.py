from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

from models import User, Bookmark

@app.route("/")
def hello():
    return "Hello World"

if __name__ == "__main__":
    app.run()
