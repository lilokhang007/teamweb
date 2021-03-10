from app import create_app
app = create_app()

from utils.models import db
db.create_all()  