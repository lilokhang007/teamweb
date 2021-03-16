from __main__ import app
from utils.types import ChoiceType
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin 
    
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
        db.Column('admins_id', db.Integer(), db.ForeignKey('admins.id')),
        db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id')))
        
class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255)) 
    
class Admins(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean()) 
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Roles', secondary=roles_users,
                            backref=db.backref('admins', lazy='dynamic'))
                            
    def is_authenticated(self):
        return True  

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, Admins, Roles)
security = Security(app, user_datastore)
             
class Highlights(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    postdate = db.Column(db.DateTime())
    title = db.Column(db.Text, unique=True, nullable=False)
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
    name = db.Column(db.Text, unique=True, nullable=False)
    selfie = db.Column(db.String)
    title = db.Column(db.Text)
    desc = db.Column(db.Text)
    email = db.Column(db.Text)
    telno = db.Column(db.Text)    

class Publications(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    category = db.Column(db.Text) 
    citation = db.Column(db.Text, unique=True)  
