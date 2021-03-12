from flask import Flask, render_template, send_from_directory 
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
add_admin_page(app)

@app.route('/static/<path:path>') 
def static_files(path): 
    return send_from_directory('/static', path) 
   
@app.route('/index') 
def index(): 
    return render_template('index.html')

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
            
if __name__ == '__main__':    
    app.run(host='0.0.0.0',port='8002')      