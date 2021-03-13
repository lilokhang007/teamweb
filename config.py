# DATABASE
DB_USER = 'alan'
DB_PW = 'lilokhang'
DB_HOST = 'localhost'
DB = 'teamweb'
SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:5432/{}'.format(DB_USER,DB_PW,DB_HOST,DB)

FLASK_SECRET_KEY = 'mySecret'