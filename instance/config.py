import os
from dotenv import load_dotenv
from os.path import join, dirname


dotenv_path = join(dirname(__file__), '../.env')
print dotenv_path
load_dotenv(dotenv_path)

print os.environ.get('DATABASE_URL')

if os.environ.get('DATABASE_URL') is None:
    print "Hello Sam"
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/tmi'
else:
    print os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
