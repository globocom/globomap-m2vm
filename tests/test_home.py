import unittest
from m2vm.app import create_app


class BaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config/test_config.py')
        cls.client = cls.app.test_client()

    def test_home_route_returns_status_code_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
