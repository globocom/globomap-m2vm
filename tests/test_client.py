from unittest import TestCase, mock
from m2vm.client import GmapClient
from m2vm.app import create_app
from datetime import datetime, timedelta
from flask import session, current_app
import requests


class ClientTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config/test_config.py')


    @mock.patch('requests.post')
    def test_getting_new_token_with_no_prior_token(self, mock_post):
        mock_post.return_value.json.return_value = {
            'data' : 'teste'
        }
        with self.app.test_request_context():
            session['token_data'] = None

            gmap_client = GmapClient()

            self.assertEqual(session['token_data'], mock_post.return_value.json.return_value)

    def test_reusing_non_expired_token(self):
        with self.app.test_request_context():
            session['token_data'] = {'expires_at' : (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'token_value' : 'AS%S715H#JB213S%JCN'}
            gmap_client = GmapClient()

            self.assertEqual(gmap_client.token_data, session['token_data'])

    @mock.patch('requests.post')
    def test_getting_new_token_with_expired_token(self, mock_post):
        mock_post.return_value.json.return_value = {
            'data' : 'teste'
        }
        with self.app.test_request_context():
            session['token_data'] = {'expires_at' : (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'token_value' : 'AS%S715H#JB213S%JCN'}
            gmap_client = GmapClient()

            self.assertEqual(session['token_data'], mock_post.return_value.json.return_value)

    @mock.patch('requests.post')
    def test_auth_throws_exception (self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError()
        with self.app.test_request_context():
            gmap_client = GmapClient()
            self.assertEqual(gmap_client.token_data, None)


    @mock.patch('requests.get')
    def test_run_query(self, mock_get):
        mock_get.return_value.json.return_value = {
            'data' : 'teste'
        }
        with self.app.test_request_context():
            session['token_data'] = {'expires_at' : (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'token_value' : 'AS%S715H#JB213S%JCN'}
            gmap_client = GmapClient()

            query_result = gmap_client.run_query('query', 'variable')

            self.assertEqual(query_result, mock_get.return_value.json.return_value)

    @mock.patch('requests.get')
    def test_find_vms(self, mock_get):
        mock_get.return_value.json.return_value = {
            'data' : 'teste'
        }
        with self.app.test_request_context():
            session['token_data'] = {'expires_at' : (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 'token_value' : 'AS%S715H#JB213S%JCN'}
            gmap_client = GmapClient()

            query_result = gmap_client.find_vms('id')

            self.assertEqual(query_result, mock_get.return_value.json.return_value)

