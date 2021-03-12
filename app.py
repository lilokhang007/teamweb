from flask import Flask, request, render_template, send_from_directory, Markup
from path import FILE_UPLOAD_DIR
import os 

def create_app():
    
    app = Flask(__name__)
    print(os.path.abspath(app._static_folder))
     
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
        print(bid)
        blog = Blogs.query.get(bid).__dict__
        print(blog)
        blog = tidy_blog(blog)
        print(blog)
         
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
                   
    app.run(host='0.0.0.0',port='8002')      