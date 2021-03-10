import imghdr
import datetime
import os
import json
from flask import flash, url_for, send_from_directory, jsonify, redirect, request, render_template
from flask_admin import Admin, expose
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_login.utils import current_user
from app import create_app
from utils.forms import LoginForm
from utils.fields import MultipleImageUploadField
from wtforms.validators import ValidationError
from wtforms.fields import TextField, DateTimeField 

app = create_app()

FILE_UPLOAD_DIR = 'docs/uploads/'

from utils.models import db, Admins, Blogs
login_manager = LoginManager(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        
        print(form.username.data)
        print(form.password.data)
        user = Admins.query.filter_by(username = form.username.data,
            password = form.password.data
        ).first() 
        
        print(user)
        
        if user is None:
            return 'Authentication Error'
          
        login_user(user)  
          
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/admin/')
       
    return render_template('login.html', title='Sign In', form=form)
    
@app.route('/logout') 
def logout(): 
    logout_user()
    return redirect('/admin/')
                        
@login_manager.user_loader 
def load_user(user):   
    return Admins.query.get(user) 

class LoginMenuLink(MenuLink):

    def is_accessible(self):
        return not current_user.is_authenticated 

class LogoutMenuLink(MenuLink):

    def is_accessible(self):
        return current_user.is_authenticated      
                
class AdminView(ModelView):  
  
    def is_accessible(self):  
        return current_user.is_authenticated 
            
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login')) 
         
class BlogView(AdminView):   
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
    admin.add_view(AdminView(Admins, db.session))
    admin.add_view(BlogView(Blogs, db.session))  
    admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
    admin.add_link(LoginMenuLink(name='Login', category='', url="/login"))
    
    app.run(host='0.0.0.0',port='8002') 