import datetime
from app import app
from config import FLASK_ADMIN_USER, FLASK_ADMIN_PW
from utils.models import db, Admins, Highlights, Pages, Members 
from utils.init_pub import pub_list
from sqlalchemy.exc import IntegrityError

def init_to_db():
  # Default datetime used in postdate
  now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

  # Default image used in imgs field
  default_img = "['../img/dr_lam_yun_fat.jpg']"
  
  init_items = [
    Admins(username=FLASK_ADMIN_USER, password=FLASK_ADMIN_PW),
    Highlights(postdate=now, title='Amazing Research', content='This is a testing research highlight.', author=FLASK_ADMIN_USER, imgs=default_img),
    Pages(type='Vision', content='This is a testing vision.'),
    Pages(type='Mission', content='This is a testing mission.'),
    Pages(type='About Us', content='This is a testing about us.'),
    Pages(type='Join', content='This is a testing join message.'),
    Members(name='Alan, Li Lok Hang', title='Research Assistant', desc='I love programming.', email='lilokhang007@gmail.com', telno='12345678', selfie=default_img),
    Members(name='Nathan, Wong Yat Chun', title='Research Assistant', desc='I love programming, too.', email='nathanyc@hku.hk', telno='12345678', selfie=default_img),
    Members(name='Jeffrey, Chang Man Hei', title='Ph.D Student', desc='I do not love programming.', email='mhjchang@connect.hku.hk', telno='12345678', selfie=default_img),
    Members(name='Lee Chun Kin', title='Programmer', desc='I really love programming.', email='leeck123@hku.hk', telno='12345678', selfie=default_img),
    *pub_list, # add all publications from init_pub   
  ]   
   
  for item in init_items:  
    try:
      db.session.add(item)
      db.session.commit() 
    except IntegrityError: 
      # catch IntegrityError for repeated initial values
      db.session.rollback()
  
