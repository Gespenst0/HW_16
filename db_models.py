from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json

app = Flask(__name__, )
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw_data_base1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    phone = db.Column(db.Text)


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    order = relationship('Order')
    executor = relationship('User')


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    address = db.Column(db.Text)
    price = db.Column(db.Text)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = relationship('User', foreign_keys=[customer_id])
    executor = relationship('User', foreign_keys=[executor_id])
    offers = relationship('Offer')


# db.create_all()
# with open("Users.json", "r") as file:
#     users_data = json.load(file)
# for item in users_data:
#     user = User(id=item['id'],
#                 first_name=item['first_name'],
#                 last_name=item['last_name'],
#                 age=item['age'],
#                 email=item['email'],
#                 role=item['role'],
#                 phone=item['phone'])
#     db.session.add(user)
#     db.session.commit()
#
#
# with open("Offers.json", "r") as file:
#     offers_data = json.load(file)
# for item in offers_data:
#     offer = Offer(id=item['id'],
#                   order_id=item['order_id'],
#                   executor_id=item['executor_id'])
#     db.session.add(offer)
#     db.session.commit()
#
#
# with open("Orders.json", encoding='utf-8') as file:
#     orders_data = json.load(file)
# for item in orders_data:
#     order = Order(id=item['id'],
#                   name=item['name'],
#                   description=item['description'],
#                   start_date=item['start_date'],
#                   end_date=item['end_date'],
#                   address=item['address'],
#                   price=item['price'],
#                   customer_id=item['customer_id'],
#                   executor_id=item['executor_id'])
#     db.session.add(order)
#     db.session.commit()
