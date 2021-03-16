from utils.models import db, Highlights, Pages, Members, Publications

def drop_table():
  for table in (Highlights, Pages, Members, Publications):
    table.__table__.drop(db.engine) 