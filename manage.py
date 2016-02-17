from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from os.path import join, dirname
from dotenv import load_dotenv
import os

from app import app, db
#Development
# app.config.from_pyfile('config.py')
#Production
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
