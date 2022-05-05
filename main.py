from flask import Flask, jsonify, request
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


def instance_users_to_dict(instance):
    """
    Serialize implementation
    """
    return {
        "id": instance.id,
        "first_name": instance.first_name,
        "last_name": instance.last_name,
        "age": instance.age,
        "email": instance.email,
        "role": instance.role,
        "phone": instance.phone,
    }


@app.route("/users")
def get_all_and_by_tours_count():
    result = []
    users = User.query.all()
    for one_user in users:
        result.append(instance_users_to_dict(one_user))
    return jsonify(result)


@app.route("/users/<int:uid>", methods=['GET'])
def get_one(uid):
    user = User.query.get(uid)
    return jsonify(instance_users_to_dict(user))


def instance_orders_to_dict(instance):
    """
    Serialize implementation
    """
    return {
        "id": instance.id,
        "name": instance.name,
        "description": instance.description,
        "start_date": instance.start_date,
        "end_date": instance.end_date,
        "address": instance.address,
        "price": instance.price,
        "customer_id": instance.customer_id,
        "executor_id": instance.executor_id,

    }


@app.route("/orders")
def get_all_orders():
    result = []
    orders = Order.query.all()
    for one_order in orders:
        result.append(instance_orders_to_dict(one_order))
    return jsonify(result)


@app.route("/orders/<int:oid>", methods=['GET'])
def get_one_order(oid):
    order = Order.query.get(oid)
    return jsonify(instance_orders_to_dict(order))


def instance_offers_to_dict(instance):
    """
    Serialize implementation
    """
    return {
        "id": instance.id,
        "order_id": instance.order_id,
        "executor_id": instance.executor_id,
            }


@app.route("/offers")
def get_all_offers():
    result = []
    offers = Offer.query.all()
    for one_offer in offers:
        result.append(instance_offers_to_dict(one_offer))
    return jsonify(result)


@app.route("/offers/<int:oid>", methods=['GET'])
def get_one_offer(oid):
    offer = Offer.query.get(oid)
    return jsonify(instance_offers_to_dict(offer))


@app.route("/offers/<int:oid>", methods=['DELETE'])
def delete_one_offer(oid):
    offer = Offer.query.get(oid)
    db.session.delete(offer)
    db.session.commit()
    return f"Предложение {offer.id} удалено"


@app.route("/orders/<int:oid>", methods=['DELETE'])
def delete_one_order(oid):
    order = Order.query.get(oid)
    db.session.delete(order)
    db.session.commit()
    return f"Заказ {order.id} удален"


@app.route("/users/<int:uid>", methods=['DELETE'])
def delete_one_user(uid):
    user = User.query.get(uid)
    db.session.delete(user)
    db.session.commit()
    return f"Пользователь {user.id} удален"


@app.route("/users", methods=['POST'])
def create_user():
    data = request.json
    user = User(
        id=data.get('id'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        age=data.get('age'),
        email=data.get('email'),
        role=data.get('role'),
        phone=data.get('phone'),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(instance_users_to_dict(user))


@app.route("/orders", methods=['POST'])
def create_order():
    data = request.json
    order = Order(
        id=data.get('id'),
        name=data.get('name'),
        description=data.get('description'),
        start_date=data.get('start_date'),
        end_date=data.get('end_date'),
        address=data.get('address'),
        price=data.get('price'),
        customer_id=data.get('customer_id'),
        executor_id=data.get('executor_id'),
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(instance_orders_to_dict(order))


@app.route("/offers", methods=['POST'])
def create_offer():
    data = request.json
    offer = Offer(
        id=data.get('id'),
        order_id=data.get('order_id'),
        executor_id=data.get('executor_id'),
        )
    db.session.add(offer)
    db.session.commit()
    return jsonify(instance_offers_to_dict(offer))


@app.route("/users/<int:uid>", methods=['PUT'])
def update_user(uid):
    user = User.query.get(uid)
    params = request.json
    user.update(params)
    return jsonify(instance_users_to_dict(user))


@app.route("/offers/<int:oid>", methods=['PUT'])
def update_offer(oid):
    offer = Offer.query.get(oid)
    params = request.json
    offer.update(params)
    return jsonify(instance_offers_to_dict(offer))


@app.route("/orders/<int:oid>", methods=['PUT'])
def update_order(oid):
    order = Order.query.get(oid)
    params = request.json
    order.update(params)
    return jsonify(instance_orders_to_dict(order))


if __name__ == "__main__":
    app.run()
