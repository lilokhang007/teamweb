# Web server
APP_HOST = '0.0.0.0'
APP_PORT = '8002'

# Database
DB_USER = 'alan'
DB_PW = 'lilokhang'
DB_HOST = 'localhost'
DB = 'teamweb'
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:5432/{}'.format(DB_USER,DB_PW,DB_HOST,DB)

# Flask Secret Key
FLASK_SECRET_KEY = 'mySecret'

# Flask Admin Interface Setup
FLASK_ADMIN_USER = 'admin'
FLASK_ADMIN_PW = 'aWeb2021!'
FLASK_ADMIN_SWATCH = 'cerulean'