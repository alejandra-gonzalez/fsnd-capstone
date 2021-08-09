import os
from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

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
  __tablename__ = 'apparelItem'

  id = Column(Integer, primary_key=True)
  target_demographic = Column(String, nullable=False)
  color = Column(String, nullable=False)
  item_name = Column(String, nullable=False)
  price = Column(Integer, nullable=False)
  released = Column(DateTime, default=None)

  orders = db.relationship('OrderItem', 
    backref=db.backref('item', lazy="joined"))

  def __init__(self, target_demographic, color, item_name, price, released):
    self.item_name = item_name
    self.target_demographic = target_demographic
    self.color = color
    self.price = price,
    self.released = released

  def format(self):
    return {
      'id': self.id,
      'item_name': self.item_name,
      'target_demographic': self.target_demographic,
      'color': self.color,
      'price': self.price,
      'released': self.released}

  def insert(self):
        db.session.add(self)
        db.session.commit()

'''
Orders
Have id, user id of the user placing the order, customer name, city and state
  to ship to, billing city and state
'''
class Order(db.Model):
  __tablename__ = 'order'

  id = Column(Integer, primary_key=True)
  user_id = Column(String)
  customer_name = Column(String, nullable=False)
  ship_city = Column(String, nullable=False)
  ship_state = Column(String, nullable=False)
  billing_city = Column(String, nullable=False)
  billing_state = Column(String, nullable=False)
  order_date = Column(DateTime, nullable=False)

  items = db.relationship('OrderItem',
    backref=db.backref('order', lazy="joined"))

  def __init__(self, user_id, customer_name, ship_city, ship_state, 
    billing_city, billing_state, order_date):
    self.user_id = user_id
    self.customer_name = customer_name
    self.ship_city = ship_city
    self.ship_state = ship_state
    self.billing_city = billing_city
    self.billing_state = billing_state
    self.order_date = order_date

  def format(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'customer_name': self.customer_name,
      'ship_city': self.ship_city,
      'ship_state': self.ship_state,
      'billing_city': self.billing_city,
      'billing_state': self.billing_state,
      'order_date': self.order_date}

'''
OrderItems
Have id, order id, item id and quantity
'''
class OrderItem(db.Model):
  __tablename__ = 'orderItem'

  id = Column(Integer, primary_key=True)
  order_id = Column(Integer, db.ForeignKey('order.id'), nullable=False)
  item_id = Column(Integer, db.ForeignKey('apparelItem.id'), nullable=False)
  quantity = Column(Integer, nullable=False, default=1)

  def __init__(self, order_id, item_id, quantity):
    self.order_id = order_id
    self.item_id = item_id
    self.quantity = quantity

  def format(self):
    return {
      'id': self.id,
      'order_id': self.order_id,
      'item_id': self.item_id,
      'quantity': self.quantity}