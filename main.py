from flask import Flask, render_template, Response, request, jsonify
import datetime
from waitress import serve
#from datetime import date
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError
from models import *
from flask_httpauth import HTTPBasicAuth
from validation_schemas import UserSchema, Order_detailsSchema, OrderSchema, MedicineSchema, CategorySchema, UserSchemaUpdate, OrderSchemaUpdate, Order_detailsSchemaUpdate, MedicineSchemaUpdate, CategorySchemaUpdate

app = Flask(__name__)
session = Session()
bcrypt = Bcrypt()
auth = HTTPBasicAuth()


@app.route("/api/v1/hello-world-<int:id>")
def hello(id):
    hello = "Hello World " + str(id)
    return render_template("index.html", hello=hello)


@auth.verify_password
def user_auth(username, password):
    try:
        user = User.get_user_by_username(username)
    except:
        return None
    if user and bcrypt.check_password_hash(user.password, password):
        return user
    else:
        return None


@app.route("/api/v1/user", methods=['POST'])
def register_user():
    # Get data from request body
    data = request.get_json()

    # Validate input data
    try:
        UserSchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    # Check if user already exists
    exists = session.query(User.id_user).filter_by(username=data['username']).first()
    exists2 = session.query(User.id_user).filter_by(email=data['email']).first()
    #exists3 = session.query(User.userId).filter_by(id_user=data['id_user']).first()
    if exists or exists2:
        return Response(status=409, response='User with such username or email or id already exists.')

    # Hash user's password
    hashed_password = bcrypt.generate_password_hash(data['password'])
    # Create new user
    new_user = User(id_user = data["id_user"], username=data['username'], first_name=data['first_name'], last_name=data['last_name'],
                    age=data['age'], email=data['email'], password=hashed_password, phone_number=data['phone_number'], userstatus=data['userstatus'])

    # Add new user to db
    session.add(new_user)
    session.commit()

    return Response(status=200, response='New user was successfully created!')


@app.route('/api/v1/user/<int:id_user>', methods=['GET'])
@auth.login_required
def get_user(id_user):
    # Check if user exists
    current = auth.current_user()
    if current.userstatus == "pharmacist" or current.id_user == id_user:
        if id_user <= 0:
            return Response(status=400, response='Invalid userId supplied.')
        db_user = User.get_user_by_id(id_user)
        if not db_user:
            return Response(status=404, response='A user with provided id was not found.')

        # Return user data
        user_data = {'id': db_user.id_user, 'username': db_user.username, 'first_name': db_user.first_name,
                     'last_name': db_user.last_name, 'age':db_user.age, 'email': db_user.email, 'phone_number': db_user.phone_number,
                     'userstatus': db_user.userstatus}
        return jsonify({"user": user_data})
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/user/<int:id_user>', methods=['PUT'])
@auth.login_required
def update_user(id_user):
    # Get data from request body
    current = auth.current_user()
    if User.is_pharmacist(current.userstatus) or current.id_user == id_user:
        data = request.get_json()

        # Check if user exists
        db_user = session.query(User).filter_by(id_user=id_user).first()
        if not db_user:
            return Response(status=404, response='A user with provided ID was not found.')

        # Check if username is not taken if user tries to change it
        if 'username' in data.keys() and db_user.username != data['username']:
            exists = session.query(User).filter_by(username=data['username']).first()
            if exists:
                return Response(status=400, response='User with such username already exists.')
            db_user.username = data['username']
        try:
            UserSchemaUpdate().load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        # Change user data
        if 'first_name' in data.keys():
            db_user.first_name = data['first_name']
        if "last_name" in data.keys():
            db_user.last_name = data['last_name']
        if "age" in data.keys():
            db_user.age = data['age']
        if "email" in data.keys() and db_user.email != data['email']:
            exists = session.query(User).filter_by(email=data['email']).first()
            if exists:
                return Response(status=400, response='User with such email already exists.')
            db_user.email = data['email']
        if 'password' in data.keys():
            hashed_password = bcrypt.generate_password_hash(data['password'])
            db_user.password = hashed_password
        if "phone_number" in data.keys():
            db_user.phone_number = data["phone_number"]
        if "userstatus" in data.keys():
            db_user.userstatus = data["userstatus"]

        # Save changes
        session.commit()

        # Return new user data
        user_data = {'id': db_user.id_user, 'username': db_user.username, 'first_name': db_user.first_name,
                     'last_name': db_user.last_name, 'age': db_user.age, 'email': db_user.email,
                     'phone_number': db_user.phone_number,
                     'userstatus': db_user.userstatus}
        return jsonify({"user": user_data})
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/user/<int:id_user>', methods=['DELETE'])
@auth.login_required
def delete_user(id_user):
    # Check if user exists
    current = auth.current_user()
    if current.userstatus == "pharmacist" or current.id_user == id_user:
        db_user = session.query(User).filter_by(id_user=id_user).first()
        if not db_user:
            return Response(status=404, response='A user with provided ID was not found.')

        # Delete user
        session.delete(db_user)
        #deleting = delete(User).where(User.id_user == id_user)
        #session.execute(deleting)
        session.commit()
        return Response(status=200, response='User was deleted.')
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route("/api/v1/category", methods=['POST'])
@auth.login_required
def add_category():
    # Get data from request body
    current = auth.current_user()
    if current.userstatus == "pharmacist":
        data = request.get_json()

        # Validate input data
        try:
            CategorySchema().load(data)
        except ValidationError as err:
            return jsonify(err.messages), 405

        # Check if user already exists
        exists = session.query(Category).filter_by(category_name=data['category_name']).first()
        if exists:
            return Response(status=405, response='Category with such name already exists.')

        #new_category = User(category_name=data['category_name'], description=data['description'])

        # Add new user to db
        new_category = Category(**data)
        session.add(new_category)
        session.commit()

        return Response(status=200, response='New category was successfully created!')
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/category/<int:id_category>', methods=['GET'])
def get_category(id_category):
    # Check if user exists
    if id_category <= 0:
        return Response(status=400, response='Invalid id')
    db_category = Category.get_category_by_id(id_category)
    if not db_category:
        return Response(status=404, response='A category with provided id was not found.')

    # Return data
    return jsonify(CategorySchema().dump(db_category))


@app.route('/api/v1/category/<int:id_category>', methods=['PUT'])
@auth.login_required
def update_category(id_category):
    # Get data from request body
    current = auth.current_user()
    if current.userstatus == "pharmacist":
        data = request.get_json()

        # Check if user exists
        db_category = session.query(Category).filter_by(id_category=id_category).first()
        if not db_category:
            return Response(status=404, response='A category with provided ID was not found.')

        # Check if username is not taken if user tries to change it
        try:
            CategorySchemaUpdate().load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        # Change user data
        if 'category_name' in data.keys():
            chek = session.query(Category).filter_by(category_name=data['category_name']).first()
            if not chek:
                if 'category_name' in data.keys():
                    db_category.category_name = data['category_name']
                if "description" in data.keys():
                    db_category.description = data['description']
            elif chek.category_name == data['category_name']:
                return Response(status=405, response='Invalid input.')

        # Save changes
        session.commit()

        # Return new data
        return jsonify(CategorySchema().dump(db_category))
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/category/<int:id_category>', methods=['DELETE'])
@auth.login_required
def delete_category(id_category):
    # Check if user exists
    current = auth.current_user()
    if current.userstatus == "pharmacist":
        db_category = session.query(Category).filter_by(id_category=id_category).first()
        if not db_category:
            return Response(status=400, response='Invalid category value.')

        # Delete
        session.delete(db_category)
        #deleting = delete(Category).where(Category.id_category == id_category)
        # session.execute(deleting)
        session.commit()
        return Response(status=200, response='Category was deleted.')
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route("/api/v1/medicine", methods=['POST'])
@auth.login_required
def add_medicine():
    # Get data from request body
    current = auth.current_user()
    if current.userstatus == "pharmacist":
        # Validate input data
        data = request.get_json()
        try:
            MedicineSchema().load(data)
        except ValidationError as err:
            return jsonify(err.messages), 405

        # Check if user already exists
        #exists = session.query(Medicine).filter_by(medicine_name=data['medicine_name']).first()
        #if exists:
        #    return Response(status=409, response='Medicine with such name already exists.')
        exists1 = session.query(Category).filter_by(id_category=data['category_id']).first()
        if not exists1:
            return Response(status=405, response='Category with such id does not exist.')

        new_medicine = Medicine(**data)

        # Add new user to db
        session.add(new_medicine)
        session.commit()

        return Response(status=200, response='New medicine was successfully created!')
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/medicine/findByStatus/<status>', methods=['GET'])
def get_medicine_by_status(status):
    # Check if user exists
    if status == "available" or status == "pending" or status == "sold":
        db_medicine = session.query(Medicine).filter_by(medicine_status=status)
        output = []
        for m in db_medicine:
            output.append({'id': m.id_medicine,
                           'name': m.medicine_name,
                           'manufacturer': m.manufacturer,
                           'medicine_description': m.medicine_description,
                           'category_id': m.category_id,
                           'price': m.price,
                           'medicine_status': m.medicine_status,
                           'demand': m.demand})
        # Return data
        return jsonify({"Medicine": output})
    else:
        return Response(status=400, response='Invalid status value.')


@app.route('/api/v1/medicine/findDemand/<int:demand>', methods=['GET'])
def get_medicine_by_demand(demand):
    if demand == 1 or demand == 0:
        db_medicine = session.query(Medicine).filter_by(demand=demand)
        output = []
        for m in db_medicine:
            output.append({'id': m.id_medicine,
                           'name': m.medicine_name,
                           'manufacturer': m.manufacturer,
                           'medicine_description': m.medicine_description,
                           'category_id': m.category_id,
                           'price': m.price,
                           'medicine_status': m.medicine_status,
                           'demand': m.demand})
        # Return data
        return jsonify({"Medicine": output})
    else:
        return Response(status=400, response='Invalid status value.')


@app.route('/api/v1/medicine/<int:id_medicine>', methods=['GET'])
def get_medicine(id_medicine):
    # Check if user exists
    if id_medicine <= 0:
        return Response(status=400, response='Invalid id')
    db_medicine = Medicine.get_medicine_by_id(id_medicine)
    if not db_medicine:
        return Response(status=404, response='A medicine with provided id was not found.')

    # Return data
    return jsonify(MedicineSchema().dump(db_medicine))


@app.route('/api/v1/medicine/<int:id_medicine>', methods=['PUT'])
@auth.login_required
def update_medicine(id_medicine):
    # Get data from request body
    current = auth.current_user()
    if current.userstatus == "pharmacist":
        data = request.get_json()

        # Check if user exists
        db_medicine = session.query(Medicine).filter_by(id_medicine=id_medicine).first()
        if not db_medicine:
            return Response(status=404, response='A medicine with provided ID was not found.')

        # Check if username is not taken if user tries to change it
        try:
            MedicineSchemaUpdate().load(data)
        except ValidationError as err:
            return jsonify(err.messages), 400
        # Change user data
        if 'medicine_name' in data.keys():
            chek = session.query(Medicine).filter_by(medicine_name=data['medicine_name']).first()
            if not chek:
                pass
            elif chek.medicine_name == data['medicine_name']:
                return Response(status=405, response='Invalid input.')
        if 'medicine_name' in data.keys():
            db_medicine.medicine_name = data['medicine_name']
        if "manufacturer" in data.keys():
            db_medicine.manufacturer = data['manufacturer']
        if "medicine_description" in data.keys():
            db_medicine.medicine_description = data['medicine_description']
        if "category_id" in data.keys():
            db_category = session.query(Category).filter_by(id_category=data['category_id']).first()
            if not db_category:
                return Response(status=405, response='Invalid category value.')
            else:
                db_medicine.category_id = data['category_id']
        if "price" in data.keys():
            db_medicine.price = data['price']
        if "medicine_status" in data.keys():
            db_medicine.medicine_status = data['medicine_status']
        if "demand" in data.keys():
            db_medicine.demand = data['demand']
        # Save changes
        session.commit()

        # Return new data
        return jsonify(MedicineSchema().dump(db_medicine))
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/medicine/<int:id_medicine>', methods=['DELETE'])
@auth.login_required
def delete_medicine(id_medicine):
    # Check if user exists
    current = auth.current_user()
    if current.userstatus == "pharmacist":
        db_medicine = session.query(Medicine).filter_by(id_medicine=id_medicine).first()
        if not db_medicine:
            return Response(status=400, response='Invalid medicine value.')
        # Delete
        session.delete(db_medicine)
        #deleting = delete(Medicine).where(Medicine.id_medicine == id_medicine)
        # session.execute(deleting)
        session.commit()
        return Response(status=200, response='Medicine was deleted.')
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/medicine/demand/<int:id_medicine>', methods=['PUT'])
def demand_medicine(id_medicine):
    db_medicine = session.query(Medicine).filter_by(id_medicine=id_medicine).first()
    if not db_medicine:
        return Response(status=405, response='Invalid input.')
    if db_medicine.demand == 1:
        return Response(status=405, response='Invalid input.')
    else:
        db_medicine.demand = 1
        session.commit()
        return Response(status=200, response='Medicine was demand.')


@app.route('/api/v1/pharmacy/inventory', methods=['GET'])
def inventory():
    # Check if user exists
    db_medicine = session.query(Medicine)
    output = []
    for m in db_medicine:
        output.append({'id': m.id_medicine,
                       'name': m.medicine_name,
                       'manufacturer': m.manufacturer,
                       'medicine_description': m.medicine_description,
                       'category_id': m.category_id,
                       'price': m.price,
                       'medicine_status': m.medicine_status,
                       'demand': m.demand})
    # Return data
    return jsonify({"Medicine": output})


@app.route("/api/v1/pharmacy/order", methods=['POST'])
@auth.login_required
def add_order():
    # Get data from request body
    current = auth.current_user()
    if current.userstatus == "pharmacist":
        return Response(status=403, response="Access denied! The operation is forbidden for you")
    else:
        data = request.get_json()
        if data["user_id"] != current.id_user:
            return Response(status=403, response="Access denied! The operation is forbidden for you")
        else:
            # Validate input data
            try:
                OrderSchema().load(data)
            except ValidationError as err:
                return jsonify(err.messages), 405

            # Check if user already exists
            #exists = session.query(Medicine).filter_by(medicine_name=data['medicine_name']).first()
            #if exists:
            #    return Response(status=409, response='Medicine with such name already exists.')
            exists1 = session.query(User).filter_by(id_user=data['user_id']).first()
            if not exists1:
                return Response(status=405, response='User with such id does not exist.')
            if datetime.datetime.strptime(data["date_of_purchase"], "%Y-%m-%d %H:%M:%S") >= datetime.datetime.strptime(data["shipData"], "%Y-%m-%d %H:%M:%S"):
                return Response(status=405, response='Invalid input.')
            if data["complete"] == 1:
                return Response(status=405, response='Invalid input.')
            if data["order_status"] == "approved" or data["order_status"] == "delivered":
                return Response(status=405, response='Invalid input.')

            new_order = Order(**data)
            # Add new user to db
            session.add(new_order)
            session.commit()

            return Response(status=200, response='New order was successfully created!')


@app.route("/api/v1/pharmacy/order/medicine", methods=['POST'])
@auth.login_required
def add_order_medicine():
    # Get data from request body
    current = auth.current_user()
    if current.userstatus == "pharmacist":
        return Response(status=403, response="Access denied! The operation is forbidden for you")
    else:
        data = request.get_json()
        db_order = session.query(Order).filter_by(id_order=data['order_id']).first()
        if db_order.user_id != current.id_user:
            return Response(status=403, response="Access denied! The operation is forbidden for you")
        else:
            # Validate input data
            try:
                Order_detailsSchema().load(data)
            except ValidationError as err:
                return jsonify(err.messages), 405
            if data["count"] <= 0:
                return Response(status=405, response='Invalid input.')
            exists1 = session.query(Order).filter_by(id_order=data['order_id']).first()
            if not exists1:
                return Response(status=405, response='Order with such id does not exist. Invalid input.')
            exists2 = session.query(Medicine).filter_by(id_medicine=data['medicine_id']).first()
            if not exists2:
                return Response(status=405, response='Medicine with such id does not exist. Invalid input.')
            order_details = session.query(Order_details).filter_by(order_id=data['order_id']).order_by(Order_details.c.medicine_id)
            for u in order_details:
                if u.medicine_id == data['medicine_id'] and u.order_id == data['order_id']:
                    #return Response(status=405, response='Invalid input')
                    res = u.count+data["count"]
                    session.execute(update(Order_details).where(Order_details.c.order_id == data['order_id'],
                                                        Order_details.c.medicine_id == data['medicine_id']).values(count=res))
                    session.commit()
                    return Response(status=200, response='Order details was added.')
            order_details = Order_details.insert().values(order_id=data["order_id"], medicine_id=data["medicine_id"], count=data["count"])
            session.execute(order_details)
            session.commit()
            return Response(status=200, response='Order details was added.')


@app.route('/api/v1/pharmacy/order/<int:id_order>/<int:id_medicine>', methods=['DELETE'])
@auth.login_required
def delete_medicine_order(id_order, id_medicine):
    # Check if user exists
    current = auth.current_user()
    db_order = session.query(Order).filter_by(id_order=id_order).first()
    if not db_order:
        return Response(status=404, response='Order not found.')
    if current.userstatus == "pharmacist" or db_order.user_id == current.id_user:
        db_medicine = session.query(Medicine).filter_by(id_medicine=id_medicine).first()
        if not db_medicine:
            return Response(status=400, response='Invalid medicine value.')
        deleting = delete(Order_details).where(Order_details.c.order_id == id_order,
                                               Order_details.c.medicine_id == id_medicine)
        session.execute(deleting)
        session.commit()
        return Response(status=200, response='Medicine was deleted.')
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/pharmacy/order/<int:id_order>/<int:id_medicine>', methods=['PUT'])
@auth.login_required
def update_order_details(id_order, id_medicine):
    current = auth.current_user()
    db_order = session.query(Order).filter_by(id_order=id_order).first()
    if not db_order:
        return Response(status=404, response='Order not found.')
    if current.userstatus == "pharmacist" or db_order.user_id == current.id_user:
        db_medicine = session.query(Medicine).filter_by(id_medicine=id_medicine).first()
        if not db_medicine:
            return Response(status=404, response='Invalid medicine value.')
        db_order_details = session.query(Order_details).filter_by(order_id=id_order, medicine_id=id_medicine).first()
        if not db_order_details or db_order_details.medicine_id != id_medicine:
            return Response(status=405, response='Invalid input.')
        data = request.get_json()
        if data["count"] <= 0:
            return Response(status=405, response='Invalid input.')
        if db_order.order_status == "approved" or db_order.order_status == "delivered" or db_order.complete == 1:
            return Response(status=405, response="Order approved or delivered or complete")
        if "count" in data.keys():
            #    db_event_participant.user_status = data["user_status"]
            session.execute(update(Order_details).where(Order_details.c.order_id == id_order,
                                                        Order_details.c.medicine_id == id_medicine).values(count=data["count"]))
        # Save changes
        session.commit()
        return Response(status=200, response='Order details was updated.')
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/pharmacy/order/<int:id_order>', methods=['GET'])
@auth.login_required
def get_order(id_order):
    # Check if user exists
    current = auth.current_user()
    db_order = session.query(Order).filter_by(id_order=id_order).first()
    if not db_order:
        return Response(status=404, response='Order not found.')
    if current.userstatus == "pharmacist" or db_order.user_id == current.id_user:
        db_order_details = session.query(Order_details).filter_by(order_id=id_order)
        output = []
        res = 0
        for d in db_order_details:
            db_medicine = session.query(Medicine).filter_by(id_medicine=d.medicine_id).first()
            res += d.count * db_medicine.price
        output.append({'id': db_order.id_order,
                       'user_id': db_order.user_id,
                       'address': db_order.address,
                       'date_of_purchase': db_order.date_of_purchase,
                       'shipData': db_order.shipData,
                       'order_status': db_order.order_status,
                       'complete': db_order.complete,
                       'total': res})
        for d in db_order_details:
            db_medicine = session.query(Medicine).filter_by(id_medicine=d.medicine_id).first()
            output.append({'Details': "order",
                           'order_id': d.order_id,
                           'medicine_id': d.medicine_id,
                           'medicine': db_medicine.medicine_name,
                           'price': db_medicine.price,
                           'count': d.count})
        # Return data
        return jsonify({"Medicine": output})
        # Return data
        #return jsonify(OrderSchema().dump(db_order))
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/pharmacy/order/<int:id_order>', methods=['PUT'])
@auth.login_required
def update_order(id_order):
    # Get data from request body
    current = auth.current_user()
    db_order = Order.get_order_by_id(id_order)
    if not db_order:
        return Response(status=404, response='Order not found.')
    if current.userstatus == "pharmacist" or db_order.user_id == current.id_user:
        data = request.get_json()
        if id_order <= 0:
            return Response(status=400, response='Invalid id.')

        # Check if order exists
        try:
            OrderSchemaUpdate().load(data)
        except ValidationError as err:
            return jsonify(err.messages), 405
        # Change data
        if "user_id" in data.keys():
            exists1 = session.query(User).filter_by(id_user=data['user_id']).first()
            if not exists1:
                return Response(status=405, response='User with such id does not exist.')

        if 'date_of_purchase' in data.keys():
            if "shipData" in data.keys():
                if datetime.datetime.strptime(data["date_of_purchase"], '%Y-%m-%d %H:%M:%S') >= datetime.datetime.strptime(data["shipData"], '%Y-%m-%d %H:%M:%S'):
                    return Response(status=405, response='Invalid input.')
            else:
                if datetime.datetime.strptime(data["date_of_purchase"], '%Y-%m-%d %H:%M:%S') >= db_order.shipData:
                    return Response(status=405, response='Invalid input.')
        elif "shipData" in data.keys():
            if db_order.date_of_purchase >= datetime.datetime.strptime(
                    data["shipData"], '%Y-%m-%d %H:%M:%S'):
                return Response(status=405, response='Invalid input.')

        if 'user_id' in data.keys():
            chek = session.query(User).filter_by(id_user=data['user_id']).first()
            if not chek:
                return Response(status=405, response='Invalid input.')
        else:
            if 'address' in data.keys():
                db_order.address = data['address']
            if "manufacturer" in data.keys():
                db_order.date_of_purchase = data['date_of_purchase']
            if "shipData" in data.keys():
                db_order.shipData = data['shipData']
            if "order_status" in data.keys():
                db_order.order_status = data['order_status']
            if "complete" in data.keys():
                db_order.complete = data['complete']
        # Save changes
        session.commit()

        # Return new data
        return jsonify(OrderSchema().dump(db_order))
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


@app.route('/api/v1/pharmacy/order/<int:id_order>', methods=['DELETE'])
@auth.login_required
def delete_order(id_order):
    # Check if user exists
    current = auth.current_user()
    db_order = session.query(Order).filter_by(id_order=id_order).first()
    if not db_order:
        return Response(status=404, response='Order not found.')
    if current.userstatus == "pharmacist" or db_order.user_id == current.id_user:
        # Delete
        session.delete(db_order)
        #deleting = delete(Order).where(Order.id_order == id_order)
        # session.execute(deleting)
        session.commit()
        return Response(status=200, response='Order was deleted.')
    else:
        return Response(status=403, response="Access denied! The operation is forbidden for you")


if __name__ == '__main__':
    #serve(app)
    app.run(debug=True)
