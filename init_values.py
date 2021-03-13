import datetime
from app import app
from utils.models import db, Admins, Highlights, Pages
from sqlalchemy.exc import IntegrityError

now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
init_items = [
  Admins(username='admin', password='aWeb2021!'),
  Highlights(postdate=now, title='Amazing Research', content='This is a testing research highlight.', author='admin'),
  Pages(type='Vision', content='This is a testing vision.'),
  Pages(type='Mission', content='This is a testing mission.'),
  Pages(type='About Us', content='This is a testing about us.'),
]

for item in init_items: 
  try:
    db.session.add(item)
    db.session.commit() 
  except IntegrityError:
    db.session.rollback()
  