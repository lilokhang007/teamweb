from config import APP_HOST, APP_PORT, SQLALCHEMY_DATABASE_URI, SECURITY_PASSWORD_SALT, FLASK_SECRET_KEY, FLASK_ADMIN_SWATCH
from flask import Flask, request, render_template, send_from_directory, Markup
from flask_bcrypt import Bcrypt 
from path import FILE_UPLOAD_DIR
import os 
import argparse

parser = argparse.ArgumentParser(description='Launch the Flask Application for the Team Web.')
parser.add_argument('-host', default=APP_HOST, help='hostname')
parser.add_argument('-port', default=APP_PORT, help='port')
args = parser.parse_args()

def create_app():  
    app = Flask(__name__)
     
    # set optional bootswatch theme   
    app.config['FLASK_ADMIN_SWATCH'] = FLASK_ADMIN_SWATCH
    app.config['SECRET_KEY'] = FLASK_SECRET_KEY
    app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = FILE_UPLOAD_DIR 
     
    return app

def add_admin_page(app = None): 
    from admin import create_admin
    admin = create_admin()
    admin.init_app(app)
    
app = create_app()
bcrypt = Bcrypt(app)
if __name__ == '__main__':
    add_admin_page(app) # add admin page to app
    
    from utils.models import Slides, Highlights, Partners, Pages, Members
    def tidy_blog(blog, img_key = 'imgs', content_key= 'content'):
        # Tidy up the values of the input dictionary
        if blog[img_key] is not None:
          blog[img_key] = [FILE_UPLOAD_DIR + img for img in eval(blog[img_key])] # set proper blog image path
        blog[content_key] = blog[content_key].replace("\n", Markup("<br></br>")) # set html tag
        return blog
        
    # Routing functions
    @app.route('/static/<path:path>') 
    def static_files(path): 
        return send_from_directory('/static', path) 
    
    @app.route('/')
    @app.route('/index')  
    def index(): 
        slides = Slides.query.all()
        slides = [tidy_blog(result.__dict__, content_key= 'desc') for result in slides] 
        blogs = Highlights.query.all()
        blogs = [tidy_blog(result.__dict__) for result in blogs] 
        partners = Partners.query.all()
        partners = [tidy_blog(result.__dict__, content_key= 'desc') for result in partners] 
                
        return render_template('index.html', slides=slides, blogs=blogs, partners=partners) 
    
    @app.route('/blogs') 
    def blog():   
        bid = request.args.get('id', default = 1, type = int)
        blog = Highlights.query.get(bid)
        if blog is not None:       
            blog = tidy_blog(blog.__dict__)
        else:
            return render_template('blog.html', blog=None)      
        return render_template('blog.html', blog=blog)  
     
    @app.route('/about') 
    def about(): 
        about = Pages.query.filter_by(type='About Us').first()
        if about is not None:
          about = tidy_blog(about.__dict__) 
        return render_template('about.html', about=about)
        
    @app.route('/vision')  
    def vision(): 
        vision = Pages.query.filter_by(type='Vision').first()
        if vision is not None:
          vision = tidy_blog(vision.__dict__)
        mission = Pages.query.filter_by(type='Mission').first()
        if mission is not None:
          mission = tidy_blog(mission.__dict__)
        return render_template('vision.html', vision=vision, mission=mission)
         
    @app.route('/contact') 
    def contact(): 
        return render_template('contact.html')
         
    @app.route('/team') 
    def team(): 
        members = Members.query.all()
        members = [tidy_blog(result.__dict__, img_key='selfie', content_key='desc') for result in members] # convert to dict list

        return render_template('team.html', members=members)
         
    @app.route('/research') 
    def research(): 
        return render_template('research.html')
        
    @app.route('/pub') 
    def pub():  
        return render_template('pub.html') 
    
    @app.route('/education') 
    def education():  
        return render_template('education.html')
    
    @app.route('/join')  
    def join():   
        join = Pages.query.filter_by(type='Join').first()
        if join is not None:
            join = tidy_blog(join.__dict__)
        return render_template('join.html', join=join)
                   
    app.run(host=args.host,port=args.port)       
