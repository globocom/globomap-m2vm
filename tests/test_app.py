from unittest import TestCase, mock
from m2vm.app import create_app
from flask import template_rendered
import re


class AppTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config/test_config.py')
        cls.client = cls.app.test_client()
        cls.api = 'dummy-gmap-api'

    def test_app_loads_test_config_module(self):
        self.assertEqual(self.app.config['ENV'], 'testing')

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

    def test_post_for_home_route_returns_a_bad_request_without_machine_parameter(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 400)

    @mock.patch('requests.get')
    def test_search_for_machine_should_render_a_list(self, get_mock):
        get_mock.return_value.json.return_value = {
            "machine": "m",
            "vms": [{'name': f'm_vm_{n:02}',
                     'ip': f'10.0.0.{n}'} for n in range(2)]
        }

        response = self.client.post('/', data={"machine": "m"})

        for key in [f'm_vm_{n:02}' for n in range(2)]:
            self.assertIn(f'{key}', response.data.decode(), 'Failed rendering mock list')

    @mock.patch('requests.get')
    def test_main_input_text_has_its_value_filled_after_a_search(self, get_mock):
        get_mock.return_value.json.return_value = {
            "machine": "m",
            "vms": [{'name': f'm_vm_{n:02}',
                     'ip': f'10.0.0.{n}'} for n in range(2)]
        }

        response = self.client.post('/', data={"machine": "m"})
        body = response.data.decode()

        match = re.search('value="', body)
        _, value = match.span()
        self.assertNotEqual(value, '"')

    def test_returns_bad_request_validation_error_with_a_long_input_query(self):
        string = 'a' * 110
        response = self.client.get(f'/{self.api}/{string}')
        self.assertEqual(response.status_code, 400)
