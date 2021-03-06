import re
from unittest import TestCase, mock
from flask import template_rendered, url_for, request
from m2vm.app import create_app


class FakeConfig:
    def from_pyfile(self, f):
        self.file = f


class FakeFlask:
    config = FakeConfig()

    def route(self, *args, **kwargs):
        def wrp(*args):
            pass
        return wrp


class AppTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config/test_config.py')
        cls.client = cls.app.test_client()

    def test_app_loads_test_config_module(self):
        self.assertEqual(self.app.config['ENV'], 'testing')

    @mock.patch('m2vm.app.Flask')
    def test_create_app_with_default_dev_config_module(self, mock_app_flask):
        mock_app_flask.return_value = FakeFlask()
        app = create_app()
        self.assertEqual(app.config.file, 'config/dev_config.py')

    def test_app_loads_default_dev_config_if_none_was_passed(self):
        api_env = self.app.config['ENV']
        if api_env != 'production' and api_env != 'testing':
            self.assertEqual(api_env, 'development')

    def test_home_route_returns_status_code_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_route_should_render_search_form(self):
        response = self.client.get('/')
        body = response.data.decode()
        self.assertIn('form', body, 'Failed to render the search form')

    def test_post_for_home_route_returns_a_bad_request_without_server_name_parameter(self):
        response = self.client.post('/', data={'server_q': None})
        self.assertEqual(response.status_code, 400)

    @mock.patch('m2vm.client.GmapClient.run_query')
    def test_search_for_server_name_should_render_a_list(self, mock_query):

        mock_query.return_value = 200, [{
            '_id': f'0as9d0{x}',
            'name': f'machine{x}',
            'properties': {'ips': ('10.0.0.1', '10.0.0.2')},
        } for x in range(3)]

        response = self.client.post('/', data={'server_q': "m"})
        body = response.data.decode()
        self.assertIn('table', body)

    @mock.patch('m2vm.client.GmapClient.run_query')
    def test_server_name_input_text_has_its_value_filled_after_a_search(self, mock_query):

        mock_query.return_value = 200, [{
            '_id': f'0as9d0{x}',
            'name': f'machine{x}',
            'properties': {'ips': ('10.0.0.1', '10.0.0.2')},
        } for x in range(3)]

        response = self.client.post('/', data={"server_q": "m"})
        body = response.data.decode()
        match = re.search('value="', body)
        _, value = match.span()
        self.assertNotEqual(value, '"')

    def test_returns_bad_request_validation_error_with_a_long_input_query(self):
        string = 'a' * 110
        response = self.client.post('/', data={'server_q': string})
        self.assertEqual(response.status_code, 400)

    @mock.patch('m2vm.client.GmapClient.run_query')
    @mock.patch('m2vm.client.GmapClient.find_vms')
    def test_return_redirect_if_only_one_server_is_found(self, mock_vms, mock_query):
        mock_query.return_value = 200, [{
            '_id': '0as9d0',
            'name': 'machine',
            'properties': {'ips': ('10.0.0.1', '10.0.0.2')},
        }]
        mock_vms.return_value = 200, {'nodes': []}

        with self.client as c:
            response = c.post('/', data={"server_q": "machine"})
            self.assertIn('location.href', response.data.decode())

    @mock.patch('m2vm.client.GmapClient.find_vms')
    def test_find_vms_with_an_empty_data(self, mock_vms):
        mock_vms.return_value = 200, {'nodes': []}
        response = self.client.get('/machine?server_id=asd87a')

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('<table', response.data.decode())

    @mock.patch('m2vm.client.GmapClient.run_query')
    def test_render_template_when_server_name_query_returns_empty(self, mock_query):
        mock_query.return_value = 200, []

        response = self.client.post('/', data={"server_q": "machine"})
        body = response.data.decode()
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('<table', body)

    def test_vms_route_with_no_server_id(self):
        response = self.client.get('/machine')
        self.assertEqual(response.status_code, 400)

    @mock.patch('m2vm.client.GmapClient.find_vms')
    def test_check_find_vms_are_rendered(self, mock_query):
        mock_query.return_value = 200, {'nodes': [
            {
                'properties': {'equipment_type': 'Servidor Virtual', 'ips': ('10.0.0.1', '10.0.0.2')},
                '_id': 'asd87a',
                'name': 'vm_name',
            }
        ]}
        response = self.client.get('/machine?server_id=asd87a')
        body = response.data.decode()
        self.assertIn('table', body)

    @mock.patch('m2vm.client.GmapClient.find_vms')
    def test_check_nodes_that_are_not_vms_are_not_rendered(self, mock_query):
        mock_query.return_value = 200, {'nodes': [
            {
                'properties': {'equipment_type': 'Servidor Virtual', 'ips': ('10.0.0.1', '10.0.0.2')},
                '_id': 'asd87a',
                'name': 'vm_name',
            },
            {
                'properties': {'equipment_type': 'Servidor', 'ips': ('10.0.0.1', '10.0.0.2')},
                '_id': 'ausaiodahsiu',
                'name': 'bad_name',
            }
        ]}
        response = self.client.get('/machine?server_id=asd87a')
        body = response.data.decode()
        self.assertNotIn('bad_name', body)

    @mock.patch('m2vm.client.GmapClient.find_vms')
    def test_find_vms_returns_more_than_399(self, mock_query):
        mock_query.return_value = 400, {'nodes': None}
        response = self.client.get('/machine?server_id=asdas3')
        self.assertEqual(response.status_code, 400)

    @mock.patch('m2vm.client.GmapClient.run_query')
    def test_run_query_returns_more_than_399(self, mock_query):
        mock_query.return_value = 400, {'nodes': None}
        response = self.client.post('/', data={'server_q': 'data'})
        self.assertEqual(response.status_code, 400)

    @mock.patch('m2vm.client.GmapClient.run_query')
    def test_search_servers_by_ip_calls_the_right_query(self, mock_query):
        mock_query.return_value = 200, {}
        _ = self.client.post('/', data={'search_type': 'by_ip', 'server_q': '10.0.0.1'})
        mock_query.assert_called_with('query_physical_servers_by_ip', '10.0.0.1')
