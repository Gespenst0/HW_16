from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db_models import Offer, Order, User
from utils import instance_orders_to_dict, instance_users_to_dict, instance_offers_to_dict

app = Flask(__name__, )
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hw_data_base1.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)


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
