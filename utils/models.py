from __main__ import app
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Admins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, index=True)
    password = db.Column(db.String(10))

    def is_authenticated(self):
        return True 
             
class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    postdate = db.Column(db.DateTime)
    title = db.Column(db.Text)
    content = db.Column(db.Text) 
    imgs = db.Column(db.String)
    author = db.Column(db.ForeignKey(Admins.username, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)  