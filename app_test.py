from base64 import b64encode
from unittest import TestCase

from main import app
from models import Session, engine
import bcrypt
import json

app.testing = True
client = app.test_client()


class BaseTestCase(TestCase):
    client = app.test_client()

    def setUp(self):
        super().setUp()

        # Users and admins data
        self.admin_1_data = {
            "id_user": 3,
            "username": "admin1",
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "age": 32,
            "email": "admin1@gmail.com",
            "password": "admin1",
            "phone_number": "0999309899",
            "userstatus": "pharmacist"
        }

        self.admin_1_data_hashed = {
            **self.admin_1_data,
            "password": bcrypt.hashpw(bytes(self.admin_1_data['password'], 'utf-8'), bcrypt.gensalt())
        }

        self.admin_1_credentials = b64encode(b"admin1:admin1").decode('utf-8')

        self.admin_2_data = {
            "id_user": 4,
            "username": "admin2",
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "age": 32,
            "email": "admin2@gmail.com",
            "password": "admin2",
            "phone_number": "0999309899",
            "userstatus": "pharmacist"
        }

        self.admin_2_data_hashed = {
            **self.admin_2_data,
            "password": bcrypt.hashpw(bytes(self.admin_2_data['password'], 'utf-8'), bcrypt.gensalt())
        }

        self.admin_2_credentials = b64encode(b"admin2:admin2").decode('utf-8')

        self.user_1_data = {
            "id_user": 1,
            "username": "user1",
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "age": 32,
            "email": "user1@gmail.com",
            "password": "user1",
            "phone_number": "0999309899",
            "userstatus": "user"
        }

        self.user_1_data_hashed = {
            **self.user_1_data,
            "password": bcrypt.hashpw(bytes(self.user_1_data['password'], 'utf-8'), bcrypt.gensalt())
        }

        self.user_1_credentials = b64encode(b"user1:user1").decode('utf-8')

        self.user_2_data = {
            "id_user": 2,
            "username": "user2",
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "age": 32,
            "email": "user2@gmail.com",
            "password": "user2",
            "phone_number": "0999309899",
            "userstatus": "user"
        }

        self.user_3_data = {
            "id_user": 5,
            "username": "us",
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "age": 32,
            "email": "user3@gmail.com",
            "password": "user3",
            "phone_number": "0999309899",
            "userstatus": "user"
        }

        self.user_2_data_hashed = {
            **self.user_2_data,
            "password": bcrypt.hashpw(bytes(self.user_2_data['password'], 'utf-8'), bcrypt.gensalt())
        }

        self.user_2_credentials = b64encode(b"user2:user2").decode('utf-8')

        # Category data
        self.category_1_data = {
            "id_category": 1,
            "category_name": "Spray",
            "description": "test1"
        }

        self.category_2_data = {
            "id_category": 2,
            "category_name": "Pills",
            "description": "test2"
        }

        self.category_3_data = {
            "id_category": 3,
            "category_name": "P",
            "description": "t"
        }

        # Medicines data
        self.medicine_1_data = {
            "id_medicine": 1,
            "medicine_name": "test1",
            "manufacturer": "HeartBeat",
            "medicine_description": "test1",
            "category_id": 2,
            "price": 2,
            "medicine_status": "available",
            "demand": False
        }

        self.medicine_2_data = {
            "id_medicine": 2,
            "medicine_name": "test2",
            "manufacturer": "HeartBeat",
            "medicine_description": "test1",
            "category_id": 2,
            "price": 20,
            "medicine_status": "available",
            "demand": 0
        }

        self.medicine_3_data = {
            "id_medicine": 3,
            "medicine_name": "t",
            "manufacturer": "HeartBeat",
            "medicine_description": "test1",
            "category_id": 2,
            "price": 20,
            "medicine_status": "available",
            "demand": 0
        }

        self.medicine_4_data = {
            "id_medicine": 4,
            "medicine_name": "tdsfbjksdf",
            "manufacturer": "HeartBeat",
            "medicine_description": "test1",
            "category_id": 10,
            "price": 20,
            "medicine_status": "available",
            "demand": False
        }

        # Orders data
        self.order_1_data = {
            "id_order": 1,
            "user_id": 1,
            "address": "yfewtuygewjhkkjhyugfuywgeuyfgyuwqgfyugqugewgfuqgyefhwg",
            "date_of_purchase": "2019-05-08 17:12:05",
            "shipData": "2020-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        }

        self.order_2_data = {
            "id_order": 2,
            "user_id": 2,
            "address": "yfewtuygewjkhhkjhkjyugfuywgeuyfgyuwqgfyugqugewgfuqgyefhwg",
            "date_of_purchase": "2019-05-08 17:12:05",
            "shipData": "2020-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        }

        self.order_3_data = {
            "id_order": 3,
            "user_id": 2,
            "address": "y",
            "date_of_purchase": "2019-05-08 17:12:05",
            "shipData": "2020-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        }

        self.order_4_data = {
            "id_order": 3,
            "user_id": 1,
            "address": "y",
            "date_of_purchase": "2020-05-08 17:12:05",
            "shipData": "2019-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        }

        # Orders-Medicines data
        self.order_medicine_1_data = {
            "order_id": 1,
            "medicine_id": 1,
            "count": 1
        }

        self.order_medicine_2_data = {
            "order_id": 2,
            "medicine_id": 2,
            "count": 1
        }

        self.order_medicine_3_data = {
            "order_id": 2,
            "medicine_id": 2,
            "count": 1
        }

    def tearDown(self):
        self.close_session()

    def close_session(self):
        Session.close()

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def get_auth_headers(self, credentials):
        return {"Authorization": f"Basic {credentials}"}

    # Methods for the database
    def clear_user_db(self):
        #engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from user;')

    def clear_category_db(self):
        #engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from category;')

    def clear_medicine_db(self):
        #engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from medicine;')

    def clear_order_db(self):
        #engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from pp.order;')

    def clear_order_medicine_db(self):
        #engine.execute('SET FOREIGN_KEY_CHECKS=0;')
        engine.execute('delete from order_details;')

    def create_all_users(self):
        self.client.post('api/v1/user', json=self.user_1_data)
        self.client.post('api/v1/user', json=self.user_2_data)
        self.client.post('api/v1/user', json=self.admin_1_data)
        self.client.post('api/v1/user', json=self.admin_2_data)

    def create_all_categories(self):
        self.client.post('/api/v1/category', json=self.category_1_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))
        self.client.post('/api/v1/category', json=self.category_2_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))

    def create_all_medicines(self):
        self.client.post('api/v1/medicine', json=self.medicine_1_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))
        self.client.post('api/v1/medicine', json=self.medicine_2_data,
                         headers=self.get_auth_headers(self.admin_1_credentials))

    def create_all_orders(self):
        self.client.post('api/v1/pharmacy/order', json=self.order_1_data,
                         headers=self.get_auth_headers(self.user_1_credentials))
        self.client.post('api/v1/pharmacy/order', json=self.order_2_data,
                         headers=self.get_auth_headers(self.user_2_credentials))

    def create_all_order_medicine_tables(self):
        self.client.post('api/v1/pharmacy/order/medicine', json=self.order_medicine_1_data,
                         headers=self.get_auth_headers(self.user_1_credentials))

        self.client.post('api/v1/pharmacy/order/medicine', json=self.order_medicine_2_data,
                         headers=self.get_auth_headers(self.user_2_credentials))


class TestUser(BaseTestCase):
    def test_create_user_1(self):
        self.clear_user_db()
        response = self.client.post('api/v1/user', json=self.user_1_data)
        self.assertEqual(response.status_code, 200)

    def test_create_not_unique_user(self):
        self.clear_user_db()
        response = self.client.post('api/v1/user', json=self.user_3_data)
        self.assertEqual(response.status_code, 400)

    def test_create_not_unique_user1(self):
        self.clear_user_db()
        self.client.post('api/v1/user', json=self.user_1_data)
        response = self.client.post('api/v1/user', json=self.user_1_data)
        self.assertEqual(response.status_code, 409)

    def test_get_user_by_id(self):
        self.clear_user_db()
        self.create_all_users()
        response = self.client.get('api/v1/user/1', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id1(self):
        self.clear_user_db()
        self.create_all_users()
        response = self.client.get('api/v1/user/1000', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_get_user_by_id2(self):
        self.clear_user_db()
        self.create_all_users()
        response = self.client.get('api/v1/user/2', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_user_by_not_existing_id(self):
        self.clear_user_db()
        self.create_all_users()
        response = self.client.get('api/v1/user/0', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_update_user(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.put('api/v1/user/2', data=json.dumps({
            "username": "user22",
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "age": 32,
            "email": "user22@gmail.com",
            "password": "user2",
            "phone_number": "0999309899",
            "userstatus": "user"
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_update_user5(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.put('api/v1/user/2', data=json.dumps({
            "username": "user22",
            "first_name": "Ivan",
            "last_name": "Petrenko",
            "age": 32,
            "email": "user22@gmail.com",
            "password": "user2",
            "phone_number": "0999309899",
            "userstatus": "user"
        }), content_type='application/json', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_update_user1(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.put('api/v1/user/2', data=json.dumps({
            "username": "us"
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_update_user2(self):
        self.clear_user_db()
        self.create_all_users()

        response = self.client.put('api/v1/user/200', data=json.dumps({
            "username": "user22"
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_update_user3(self):
        self.clear_user_db()
        self.create_all_users()
        response = self.client.put('api/v1/user/1', data=json.dumps({
            "username": "user2"
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_update_user4(self):
        self.clear_user_db()
        self.create_all_users()
        response = self.client.put('api/v1/user/1', data=json.dumps({
            "email": "user2@gmail.com"
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_delete_user(self):
        self.clear_user_db()
        self.create_all_users()
        response = self.client.delete('api/v1/user/1', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_not_existing_user(self):
        self.clear_user_db()
        self.create_all_users()
        response = self.client.delete('api/v1/user/10000', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)


class TestCategory(BaseTestCase):
    def test_create_category(self):
        self.clear_category_db()
        response = self.client.post('api/v1/category', json=self.category_1_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_create_category1(self):
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.post('api/v1/category', json=self.category_1_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 405)

    def test_create_category2(self):
        self.clear_category_db()
        response = self.client.post('api/v1/category', json=self.category_3_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 405)

    def test_create_category_access_denied(self):
        self.clear_category_db()
        response = self.client.post('api/v1/category', json=self.category_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_category(self):
        self.clear_category_db()
        self.create_all_categories()

        response = self.client.get('api/v1/category/0',
                                      headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_get_category1(self):
        self.clear_category_db()
        self.create_all_categories()

        response = self.client.get('api/v1/category/8',
                                      headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_delete_category(self):
        self.clear_category_db()
        self.create_all_categories()

        response = self.client.delete('api/v1/category/1',
                                      headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_category1(self):
        self.clear_category_db()
        self.create_all_categories()

        response = self.client.delete('api/v1/category/100',
                                      headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_delete_category_access_denied(self):
        self.clear_category_db()
        self.create_all_categories()

        response = self.client.delete('api/v1/category/1',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_update_category(self):
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.put('api/v1/category/2', data=json.dumps({
            "category_name": "user22",
            "description": "Ivan",
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_update_category1(self):
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.put('api/v1/category/2', data=json.dumps({
            "category_name": "user22",
            "description": "Ivan",
        }), content_type='application/json', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_update_category2(self):
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.put('api/v1/category/100', data=json.dumps({
            "category_name": "user22",
            "description": "Ivan",
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_update_category3(self):
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.put('api/v1/category/1', data=json.dumps({
            "category_name": "u",
            "description": "Ivan",
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_update_category4(self):
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.put('api/v1/category/1', data=json.dumps({
            "category_name": "Pills",
            "description": "Ivan",
        }), content_type='application/json', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 405)


class TestMedicine(BaseTestCase):
    def test_create_medicine(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.post('api/v1/medicine', json=self.medicine_1_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_create_not_unique_medicine(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.post('api/v1/medicine', json=self.medicine_3_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 405)

    def test_create_not_unique_medicine1(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.post('api/v1/medicine', json=self.medicine_4_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 405)

    def test_create_medicine_access_denied(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        response = self.client.post('api/v1/medicine', json=self.medicine_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_medicine_by_status(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.get('api/v1/medicine/findByStatus/available')
        self.assertEqual(response.status_code, 200)

    def test_get_medicine_by_status1(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.get('api/v1/medicine/findByStatus/avfhdjklable')
        self.assertEqual(response.status_code, 400)

    def test_get_medicine_by_demand(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.get('/api/v1/medicine/findDemand/0')
        self.assertEqual(response.status_code, 200)

    def test_get_medicine_by_demand1(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.get('/api/v1/medicine/findDemand/111')
        self.assertEqual(response.status_code, 400)

    def test_get_medicine_by_id(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.get('api/v1/medicine/1')
        self.assertEqual(response.status_code, 200)

    def test_get_medicine_by_id8(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.get('/api/v1/pharmacy/inventory')
        self.assertEqual(response.status_code, 200)

    def test_get_not_existing_medicine_by_id(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.get('api/v1/medicine/1000')
        self.assertEqual(response.status_code, 404)

    def test_get_not_existing_medicine_by_id1(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.get('api/v1/medicine/0')
        self.assertEqual(response.status_code, 400)

    def test_delete_medicine(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.delete('api/v1/medicine/1', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_not_existing_medicine(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.delete('api/v1/medicine/10000', headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_delete_medicine_access_denied(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.delete('api/v1/medicine/1', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_update_medicine1(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.put('api/v1/medicine/1', data=json.dumps({
            "medicine_name": "test222",
            "manufacturer": "HeartBeat1",
            "medicine_description": "test11",
            "category_id": 2,
            "price": 20,
            "medicine_status": "available",
            "demand": False
        }),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_update_medicine(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.put('api/v1/medicine/1', data=json.dumps({
            "category": 1,
            "manufacturer": "HeartBeat222",
            "name": "Cardiomagnil22",
            "status": "available22"
        }),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_update_not_existing_medicine(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()

        response = self.client.put('api/v1/medicine/1000', data=json.dumps({"manufacturer": "Phaizer"}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_update_medicine_access_denied(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.put('api/v1/medicine/1', data=json.dumps({"manufacturer": "Phaizer"}),
                                   content_type='application/json',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_add_medicine_to_demand(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.put('api/v1/medicine/demand/1')
        self.assertEqual(response.status_code, 200)

    def test_add_not_existing_medicine_to_demand(self):
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        response = self.client.put('api/v1/medicine/demand/1000',)
        self.assertEqual(response.status_code, 405)


class TestOrder(BaseTestCase):
    def test_create_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        response = self.client.post('api/v1/pharmacy/order', json=self.order_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_create_not_unique_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        response = self.client.post('api/v1/pharmacy/order', json=self.order_3_data,
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 405)

    def test_create_order_access_denied(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        response = self.client.post('api/v1/pharmacy/order', json=self.order_1_data,
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_create_order_access_denied1(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        response = self.client.post('api/v1/pharmacy/order', json=self.order_4_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 405)

    def test_add_medicine_to_order(self):
        self.clear_user_db()
        self.clear_order_db()
        self.clear_order_medicine_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_users()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.post('api/v1/pharmacy/order/medicine', json=self.order_medicine_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_add_medicine_to_order1(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        response = self.client.post('api/v1/pharmacy/order/medicine', json=self.order_medicine_1_data,
                                    headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 405)

    def test_add_medicine_to_order11(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        response = self.client.post('api/v1/pharmacy/order/medicine', json=self.order_medicine_1_data,
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_add_medicine_to_order2(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        response = self.client.post('api/v1/pharmacy/order/medicine', json=self.order_medicine_1_data,
                                    headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_add_medicine_to_order3(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        response = self.client.post('api/v1/pharmacy/order/medicine', json=self.order_medicine_3_data,
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 405)

    def test_add_medicine_to_order_access_denied(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_category_db()
        self.clear_medicine_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        response = self.client.post('api/v1/pharmacy/order/medicine', json=self.order_medicine_1_data,
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_add_medicine_to_not_existing_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        response = self.client.post('api/v1/pharmacy/order/medicine', json={
            "order_id": 2,
            "medicine_id": 1000,
            "count": 1
        },
            headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 405)

    def test_add_medicine_to_not_existing_order1(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        response = self.client.post('api/v1/pharmacy/order/medicine', json={
            "order_id": 2,
            "medicine_id": 1,
            "count": 0
        },
                                    headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 405)

    def test_delete(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.delete('api/v1/pharmacy/order/1/1', headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 400)

    def test_test_delete1(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.delete('api/v1/pharmacy/order/1/1', headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_test_delete2(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.delete('api/v1/pharmacy/order/10000/1', headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 404)

    def test_update_details(self):
        self.clear_user_db()
        self.clear_order_db()
        self.clear_order_medicine_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_users()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.put('/api/v1/pharmacy/order/2/2', json={"count": 10},
                                   headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 200)

    def test_update_details1(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.put('/api/v1/pharmacy/order/1/1', json={
            "count": 10
        }, headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_update_details3(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.put('api/v1/pharmacy/order/1/100', json={
            "count": 10
        }, headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_get_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.get('api/v1/pharmacy/order/1',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_order1(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.get('api/v1/pharmacy/order/100',
                                   headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_get_order3(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.get('api/v1/pharmacy/order/1',
                                   headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_order_update(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.put('api/v1/pharmacy/order/1', json = {
            "user_id": 1,
            "address": "ysd,mglemdklgklsdgkllkre",
            "date_of_purchase": "2019-05-08 17:12:05",
            "shipData": "2020-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        },
            headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_order_update1(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.put('api/v1/pharmacy/order/1000', json = {
            "user_id": 1,
            "address": "ysd,mglemdklgklsdgkllkre",
            "date_of_purchase": "2019-05-08 17:12:05",
            "shipData": "2020-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        },
            headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_get_order_update3(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.put('api/v1/pharmacy/order/2', json = {
            "user_id": 1,
            "address": "ysd,mglemdklgklsdgkllkre",
            "date_of_purchase": "2019-05-08 17:12:05",
            "shipData": "2020-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        },
            headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 403)

    def test_get_order_update4(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.put('api/v1/pharmacy/order/1', json = {
            "address": "ysd,mglemdklgklsdgkllkre",
            "date_of_purchase": "2019-05-08 17:12:05",
            "shipData": "2020-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        },
            headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_get_order_update5(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.put('api/v1/pharmacy/order/1', json = {
            "address": "ysd,mglemdklgklsdgkllkre",
            "shipData": "2019-05-08 17:12:05",
            "order_status": "placed",
            "complete": 0
        },
            headers=self.get_auth_headers(self.admin_1_credentials))
        self.assertEqual(response.status_code, 405)

    def test_delete_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.delete('api/v1/pharmacy/order/1',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 200)

    def test_delete_not_existing_order(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.delete('api/v1/pharmacy/order/1000',
                                      headers=self.get_auth_headers(self.user_1_credentials))
        self.assertEqual(response.status_code, 404)

    def test_delete_order_access_denied(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.delete('api/v1/pharmacy/order/1',
                                      headers=self.get_auth_headers(self.user_2_credentials))
        self.assertEqual(response.status_code, 403)

    def test_hello(self):
        self.clear_order_db()
        self.clear_user_db()
        self.clear_medicine_db()
        self.clear_category_db()
        self.create_all_categories()
        self.create_all_medicines()
        self.create_all_users()
        self.create_all_orders()
        self.create_all_order_medicine_tables()
        response = self.client.get('/api/v1/hello-world-5')
        self.assertEqual(response.status_code, 200)