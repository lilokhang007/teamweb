from flask import Flask

def create_app():
    
    app = Flask(__name__)
    app._static_folder = '' 
    
    # set optional bootswatch theme  
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://alan:lilokhang@localhost:5432/teamweb'
    app.config['SECRET_KEY'] = 'mySecret'
    
    return app
    
create_app() 