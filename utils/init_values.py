import datetime
from app import app
from config import FLASK_ADMIN_USER, FLASK_ADMIN_PW
from utils.models import db, Admins, Highlights, Pages, Members
from sqlalchemy.exc import IntegrityError

def init_to_db():
  now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
  default_img = "['../img/dr_lam_yun_fat.jpg']"
  
  init_items = [
    Admins(username=FLASK_ADMIN_USER, password=FLASK_ADMIN_PW),
    Highlights(postdate=now, title='Amazing Research', content='This is a testing research highlight.', author=FLASK_ADMIN_USER, imgs=default_img),
    Pages(type='Vision', content='This is a testing vision.'),
    Pages(type='Mission', content='This is a testing mission.'),
    Pages(type='About Us', content='This is a testing about us.'),
    Members(name='Li Lok Hang', title='Research Assistant', desc='I love programming.', email='lilokhang007@gmail.com', telno='12345678')
  ] 
  
  for item in init_items: 
    try:
      db.session.add(item)
      db.session.commit() 
    except IntegrityError: 
      db.session.rollback()
  