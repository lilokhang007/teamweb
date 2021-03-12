from flask import Flask, request, render_template, send_from_directory, Markup
from path import FILE_UPLOAD_DIR
import os 
import argparse

parser = argparse.ArgumentParser(description='Launch the Flask Application for the Team Web.')
parser.add_argument('-host', default='0.0.0.0', help='hostname')
parser.add_argument('-port', default='8002', help='port')
args = parser.parse_args()

def create_app():  
    
    app = Flask(__name__)
     
    # set optional bootswatch theme   
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alan:lilokhang@localhost:5432/teamweb'
    app.config['SECRET_KEY'] = 'mySecret'
    app.config['UPLOAD_FOLDER'] = FILE_UPLOAD_DIR
    
    return app

def add_admin_page(app = None): 
    from admin import create_admin
    admin = create_admin()
    admin.init_app(app)
        
app = create_app()
if __name__ == '__main__':
    add_admin_page(app)
    
    from utils.models import Blogs
    def tidy_blog(blog):
        blog['imgs'] = [FILE_UPLOAD_DIR + img for img in eval(blog['imgs'])] # set proper blog image path
        blog['content'] = blog['content'].replace("\n", Markup("<br></br>")) # set html tag
        return blog
        
    @app.route('/static/<path:path>') 
    def static_files(path): 
        return send_from_directory('/static', path) 
       
    @app.route('/index')  
    def index(): 
        results = Blogs.query.all()
        blogs = [result.__dict__ for result in results] # convert to dict list
        for blog in blogs:
            blog = tidy_blog(blog)
        return render_template('index.html', blogs=blogs)
    
    @app.route('/blogs') 
    def blog():   
        bid = request.args.get('id', default = 1, type = int)
        blog = Blogs.query.get(bid)
        if blog is not None:       
            blog = tidy_blog(blog.__dict__)   
        else:
            return render_template('blog.html', blog=None)      
        return render_template('blog.html', blog=blog)  
     
    @app.route('/about') 
    def about():  
        return render_template('about.html')
        
    @app.route('/vision') 
    def vision(): 
        return render_template('vision.html')
        
    @app.route('/contact') 
    def contact(): 
        return render_template('contact.html')
        
    @app.route('/team') 
    def team(): 
        return render_template('team.html')
        
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
        return render_template('join.html')
                   
    app.run(host=args.host,port=args.port)       