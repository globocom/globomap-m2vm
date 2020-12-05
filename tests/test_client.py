from datetime import datetime, timedelta
from unittest import TestCase, mock
from flask import session
from requests.exceptions import HTTPError
from m2vm.app import create_app
from m2vm.client import GmapClient


class FakeAuthResponse:

    def __init__(self, token=None, expires_at=None):
        self.token = token or 'tokentest'
        one_hour = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        self.expires_at = expires_at or one_hour

    def json(self):
        return {'token': self.token, 'expires_at': self.expires_at}


class ClientTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config/test_config.py')
        cls.client = cls.app.test_client()

        post_mock = mock.patch('requests.post').start()
        post_mock.return_value = FakeAuthResponse()

    @classmethod
    def tearDownClass(cls):
        mock.patch.stopall()

    def test_authenticated_gmapclient_instance(self):
        with self.app.test_request_context():
            gmap_client = GmapClient()
            token = gmap_client.token_data.get('token')
            self.assertEqual(token, 'tokentest')

    def test_session_with_saved_token_data(self):
        with self.app.test_request_context():
            self.assertNotIn('token_data', session)
            GmapClient()
            self.assertIn('token_data', session)

    def test_client_renew_expired_token(self):
        expired = (datetime.now() + timedelta(hours=-1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        with self.app.test_request_context():
            session['token_data'] = {'token': 'expiredtoken', 'expires_at': expired}
            gmap_client = GmapClient()
            token = gmap_client.token_data.get('token')
            self.assertEqual(token, 'tokentest')

    @mock.patch('requests.post')
    def test_globomap_api_auth_exception(self, post_mock):
        post_mock.side_effect = HTTPError()
        with self.app.test_request_context():
            gmap_client = GmapClient()
            self.assertEqual(gmap_client.token_data, None)

    @mock.patch('requests.get')
    def test_run_query_return(self, get_mock):
        get_mock.return_value.status_code = 200
        get_mock.return_value.json.return_value = {}

        with self.app.test_request_context():
            query = GmapClient().run_query('q_name', 'var')
            self.assertEqual(query, (200, {}))

    @mock.patch('requests.get')
    def test_find_vms_return(self, get_mock):
        get_mock.return_value.status_code = 200
        get_mock.return_value.json.return_value = {}

        with self.app.test_request_context():
            query = GmapClient().find_vms('id')
            self.assertEqual(query, (200, {}))
