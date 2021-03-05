import imghdr
import datetime
import os
from flask import Flask, url_for, send_from_directory, redirect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from utils.fields import MultipleImageUploadField
from utils.models import *
from wtforms.validators import ValidationError
from wtforms.fields import TextField, DateTimeField

app = Flask(__name__)

# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alan:lilokhang@localhost:5432/teamweb'
app.config['SECRET_KEY'] = 'mySecret'

FILE_UPLOAD_DIR = 'docs/uploads/'

db = SQLAlchemy(app)

class Admins(db.Model):
    username = db.Column(db.String(10), primary_key=True)
    password = db.Column(db.String(10))
    
class Blogs(db.Model):
    postdate = db.Column(db.DateTime, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    imgs = db.Column(db.String)
    author = db.Column(db.ForeignKey(Admins.username, ondelete='CASCADE', onupdate='CASCADE'), nullable=False)


login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.login'

@login_manager.user_loader
def load_user(user_id):
    return Admins.get(user_id)
        
class BlogView(ModelView):
    def prefix_name(obj, file_data):
        return file_data.filename
        
    column_exclude_list = ['imgs',]
    form_extra_fields = {
        'postdate': DateTimeField(),
        'author': TextField(),
        'imgs': MultipleImageUploadField(
            'Images',
            base_path = FILE_UPLOAD_DIR,
            thumbnail_size=(100, 100, True),
            namegen=prefix_name, 
        )
    }  

@app.route('/static/<name>')
def static_file(name):
    return send_from_directory(FILE_UPLOAD_DIR, name)  
    
if __name__ == '__main__':
    admin = Admin(app, name='Team Webpage Admin Page', template_mode='bootstrap3')
    # administrative views
    admin.add_view(ModelView(Admins, db.session))
    admin.add_view(BlogView(Blogs, db.session)) 
    
    app.run(host='0.0.0.0',port='8002') 