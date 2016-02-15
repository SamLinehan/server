from app import db
from sqlalchemy.dialects.postgresql import JSON

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
        return '<id {}>'.format(self.id)

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
