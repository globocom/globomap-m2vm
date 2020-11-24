import unittest
from m2vm.app import create_app


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config/test_config.py')
        cls.client = cls.app.test_client()
        cls.api = 'dummy-gmap-api'

    def test_home_route_returns_status_code_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class LongInputTest (BaseTest):

    def test_long_input_query_returns_status_code_200(self):
        string = 'a' * 1500
        response = self.client.get(f'/{self.api}/{string}')
        self.assertEqual(response.status_code, 200)


class NullInputTest (BaseTest):

    def test_null_input_returns_status_code_400(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 400)
