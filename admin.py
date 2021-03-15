from __main__ import app
from flask import flash, url_for, send_from_directory, jsonify, redirect, request, render_template
from flask_admin import Admin, expose
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required
from utils.forms import LoginForm
from utils.links import LoginMenuLink, LogoutMenuLink
from utils.views import AdminView, HighlightView, PageView, MemberView
from utils.models import db, Admins, Highlights, Pages, Members, Publications          
from path import FILE_UPLOAD_DIR 

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    form = LoginForm()
    
    if form.validate_on_submit():
        # Match the form input with the database
        user = Admins.query.filter_by(username = form.username.data,
            password = form.password.data
        ).first() 
        
        if user is None:
            flash('Authentication Error!')
            return render_template('login.html', title='Sign In', form=form)
          
        login_user(user)  
          
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/admin/')
       
    return render_template('login.html', title='Sign In', form=form)
    
@app.route('/logout') 
def logout(): 
    logout_user()
    return redirect('/admin/')

login_manager = LoginManager(app) 
@login_manager.user_loader 
def load_user(user):   
    return Admins.query.get(user)

def create_admin():
    admin = Admin(name='Team Webpage Admin Page', template_mode='bootstrap3') 
    # administrative views
    admin.add_view(AdminView(Admins, db.session))
    admin.add_view(HighlightView(Highlights, db.session))  
    admin.add_view(PageView(Pages, db.session))
    admin.add_view(MemberView(Members, db.session))
    admin.add_view(AdminView(Publications, db.session))
    admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
    admin.add_link(LoginMenuLink(name='Login', category='', url="/login"))
    admin.add_link(MenuLink(name='Return to the Site', category='', url="/index"))
    return admin