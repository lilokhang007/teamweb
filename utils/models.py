from __main__ import app
from utils.types import ChoiceType
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Admins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False, index=True)
    password = db.Column(db.String(10), nullable=False)

    def is_authenticated(self):
        return True 
             
class Highlights(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    postdate = db.Column(db.DateTime)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False) 
    imgs = db.Column(db.String, nullable=False)
    author = db.Column(db.ForeignKey(Admins.username, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)  
        
PageTypes = [
    ("Vision", "Vision"),
    ("Mission", "Mission"),
    ("About Us", "About Us"),
    ("Join", "Join"),
] 

class Pages(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    type = db.Column(
        ChoiceType(dict(PageTypes)), unique=True, nullable=False 
    )
    content = db.Column(db.Text)  
    imgs = db.Column(db.String) 
    
class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.Text, nullable=False)
    selfie = db.Column(db.String)
    title = db.Column(db.Text)
    desc = db.Column(db.Text)
    email = db.Column(db.Text)
    telno = db.Column(db.Text)    

class Publications(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    category = db.Column(db.Text) 
    citation = db.Column(db.Text, unique=True)  
