import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, ApparelItem, Order, OrderItem

class SkylightTestCase(unittest.TestCase):
    def setUp(self):
        self.staff_token = os.environ['staff_token']
        self.customer_token = os.environ['customer_token']
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.VALID_NEW_ITEM = {
            "item_name": "Scoop Neck Cropped Tee",
            "target_demographic": "Women",
            "color": "red",
            "price": 15,
            "released": "2021-03-15 12:05:57.10558"
        }

        self.INVALID_NEW_ITEM = {
            "target_demographic": "Women",
            "color": "brown",
            "price": 15,
            "released": "2021-03-15 12:05:57.10558"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        ''' Executed after each test '''
        pass

    def test_get_apparelItems_success(self):
        header_obj = {
            'Authorization': "Bearer {}".format(self.staff_token)
        }
        res = self.client().get('/apparel', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["apparel_items"]), type([]))

    def test_get_apparelItems_fail(self):
        header_obj = {
            'Authorization': "Bearer "
        }
        res = self.client().get('/apparel', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['error'])
        self.assertEqual(data['success'], False)

    def test_get_orders_success(self):
        header_obj = {
            'Authorization': "Bearer {}".format(self.staff_token)
        }
        res = self.client().get('/orders', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["orders"]), type([]))

    def test_get_orders_fail(self):
        header_obj = {
            'Authorization': "Bearer {}".format(self.customer_token)
        }
        res = self.client().get('/orders', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertTrue(data['error'])
        self.assertEqual(data['success'], False)

    def test_create_item_success(self):
        res = self.client().post('/apparel', headers={
            'Authorization': "Bearer {}".format(self.staff_token)
        }, json=self.VALID_NEW_ITEM)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('ApparelItem', data)

    def test_create_item_fail(self):
        res = self.client().post('/apparel', headers={
            'Authorization': "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkctTDdnYzIxbTJfWExpTUpCbEk0SSJ9.eyJpc3MiOiJodHRwczovL2FsZXgtZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjA5NDAxMThlMzg2ZDIwMDY5NGU3NTc3IiwiYXVkIjoic2t5bGlnaHQiLCJpYXQiOjE2Mjg4MTYwNTEsImV4cCI6MTYyODgyMzI1MSwiYXpwIjoiajdITWlGZEh5U0FtZUpFUUdOcXFoZ2IzSXFudmNBVVAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTppdGVtcyIsImdldDppdGVtcyIsImdldDpvcmRlcnMiLCJwYXRjaDppdGVtcyIsInBvc3Q6aXRlbXMiXX0.IHPC9qsslcCG01zJ-AaGaAb9yry3IsTV9ayDhbgdAiNEZgWczTAH0caaDg-hS3kOB82ESXxkgcSB3H5t6OpAElJitdTPMoXpoe_MVY9UTEx91i7EVkiLShvd9FHVVCygEUxJ5k6WYvbz3VrKpchGQjDVeHvlfOEEc33_PYHVcYB8G61HWEKnhvTPT1E9CH_2IaVBZnrhVQx9DcHJYJZaBeFPypRljXCJm1I1-3frqWyWA6aJp1wzHAH77WLtBhB_QmfMhNhcUNWtgoErl5xbKoZdeP4wfagBYDoBoF0XahTErEi2-eVBswR3n3MCV9IK1msoIo_IdpPbQc6xGPtZ9w"
        }, json=self.INVALID_NEW_ITEM)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertTrue(data['error'])
        self.assertEqual(data['success'], False)

if __name__ == "__main__":
    unittest.main()