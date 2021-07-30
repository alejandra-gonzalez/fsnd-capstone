import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
ApparelItem
Have target demographic, colors, name
'''
class ApparelItem(db.Model):  
  __tablename__ = 'ApparelItems'

  id = Column(Integer, primary_key=True)
  target_demographic = Column(String)
  colors = Column(String)
  item_name = Column(String)

  def __init__(self, target_demographic, colors, item_name):
    self.item_name = item_name
    self.target_demographic = target_demographic
    self.colors = colors

  def format(self):
    return {
      'id': self.id,
      'item_name': self.item_name,
      'target_demographic': self.target_demographic,
      'colors': self.colors}