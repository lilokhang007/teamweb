from app import app
from utils.models import db
from utils.init_values import init_to_db

db.create_all() # create models
init_to_db() # make initial values to tables 