from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from lists import users, offers, orders

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# user class/model
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    age = db.Column(db.Integer)
    email = db.Column(db.Text)
    role = db.Column(db.Text)
    phone = db.Column(db.Text)


# offer class/model
class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    order = db.relationship("Order")
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")


# order class/model
class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    start_date = db.Column(db.Text)
    end_date = db.Column(db.Text)
    address = db.Column(db.Text)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey(f"{User.__tablename__}.id"))


db.create_all()
# adds users to the db
for user in users:
    user_add = User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone'])
    db.session.add(user_add)
    db.session.commit()

# adds orders to the db
for order in orders:
    order_add = Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=order['start_date'],
        end_date=order['end_date'],
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id'])
    db.session.add(order_add)
    db.session.commit()

# adds offers to the db
for offer in offers:
    offer_add = Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id'])
    db.session.add(offer_add)
    db.session.commit()


# makes a page of all users
@app.route("/users/")
def get_users():
    result = []
    users_list = User.query.all()
    for user_ in users_list:
        result.append({
            "id": user_.id,
            "first_name": user_.first_name,
            "last_name": user_.last_name,
            "age": user_.age,
            "email": user_.email,
            "role": user_.role,
            "phone": user_.phone
        })
    return jsonify(result)


# makes a page of one user
@app.route("/users/<uid>/")
def get_user(uid):
    user_ = User.query.get(uid)
    return jsonify({
        "id": user_.id,
        "first_name": user_.first_name,
        "last_name": user_.last_name,
        "age": user_.age,
        "email": user_.email,
        "role": user_.role,
        "phone": user_.phone
    })


# creates a user
@app.route("/users/create/", methods=['GET', 'POST'])
def create_user():
    new_user = User(first_name='Test',
                    last_name='Test',
                    age=1,
                    email='email@email.com',
                    role='Test',
                    phone=1)
    db.session.add(new_user)
    db.session.commit()
    return "new user added"


# updates an existing user
@app.route("/users/<uid>/update/", methods=['GET', 'PUT'])
def update_user(uid):
    user_ = User.query.get(uid)
    user_.first_name = 'first_name'
    user_.last_name = 'last_name'
    user_.age = 1
    user_.email = 'email@email.com'
    user_.role = 'test'
    user_.phone = 1
    db.session.commit()
    return 'info updated'


# deletes a user
@app.route("/users/<uid>/delete/", methods=['GET', 'DELETE'])
def delete_user(uid):
    user_ = User.query.get(uid)
    user_name = f"{user_.first_name} {user_.last_name}"
    db.session.delete(user_)
    db.session.commit()
    return f"user {user_name}: removed"


# makes a page for all orders
@app.route("/orders/")
def get_orders():
    result = []
    orders_list = Order.query.all()
    for order_ in orders_list:
        result.append({
            "id": order_.id,
            "name": order_.name,
            "description": order_.description,
            "start_date": order_.start_date,
            "end_date": order_.end_date,
            "address": order_.address,
            "price": order_.price,
            "customer_id": order_.customer_id,
            "executor_id": order_.executor_id
        })
    return jsonify(result)


# makes a page for one order
@app.route("/orders/<oid>/")
def get_order(oid):
    order_ = Order.query.get(oid)
    return jsonify({
        "id": order_.id,
        "name": order_.name,
        "description": order_.description,
        "start_date": order_.start_date,
        "end_date": order_.end_date,
        "address": order_.address,
        "price": order_.price,
        "customer_id": order_.customer_id,
        "executor_id": order_.executor_id
    })


# creates an order
@app.route("/orders/create/", methods=['GET', 'POST'])
def create_order():
    new_order = Order(name='Test',
                      description='Test',
                      start_date='1.1.1.',
                      end_date='1.1.1',
                      address='Test',
                      price=1,
                      customer_id=1,
                      executor_id=1)
    db.session.add(new_order)
    db.session.commit()
    return "new order added"


# updates an existing order
@app.route("/orders/<oid>/update/", methods=['GET', 'PUT'])
def update_order(oid):
    order_ = Order.query.get(oid)
    order_.name = 'name'
    order_.description = 'description'
    order_.start_date = '1.1.1'
    order_.end_date = '1.1.1'
    order_.address = 'test'
    order_.price = 1
    order_.customer_id = 1
    order_.executor_id = 1
    db.session.commit()
    return 'info updated'


# deletes an order
@app.route("/orders/<oid>/delete/", methods=['GET', 'DELETE'])
def delete_order(oid):
    order_ = Order.query.get(oid)
    db.session.delete(order_)
    db.session.commit()
    return f"order {oid}: removed"


# makes a page for all offers
@app.route("/offers/")
def get_offers():
    result = []
    offers_list = Offer.query.all()
    for offer_ in offers_list:
        result.append({
            "id": offer_.id,
            "order_id": offer_.order_id,
            "executor_id": offer_.executor_id
        })
    return jsonify(result)


# makes a page for one offer
@app.route("/offers/<offer_id>/")
def get_offer(offer_id):
    offer_ = Offer.query.get(offer_id)
    return jsonify({
        "id": offer_.id,
        "order_id": offer_.order_id,
        "executor_id": offer_.executor_id
    })


# creates an offer
@app.route("/offers/create/", methods=['GET', 'POST'])
def create_offer():
    new_offer = Offer(order_id=1,
                      executor_id=1)
    db.session.add(new_offer)
    db.session.commit()
    return "new offer added"


# updates an existing offer
@app.route("/offers/<offer_id>/update/", methods=['GET', 'PUT'])
def update_offer(offer_id):
    offer_ = Offer.query.get(offer_id)
    offer_.order_id = 1
    offer_.executor_id = 2
    db.session.commit()
    return 'info updated'


# deletes an offer
@app.route("/offers/<offer_id>/delete/", methods=['GET', 'DELETE'])
def delete_offer(offer_id):
    offer_ = Offer.query.get(offer_id)
    db.session.delete(offer_)
    db.session.commit()
    return f"offer {offer_id}: removed"


if __name__ == '__main__':
    app.run(debug=True)
