from unittest import TestCase, mock
from m2vm.app import create_app


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('config/test_config.py')
        cls.client = cls.app.test_client()
        cls.api = 'dummy-gmap-api'

    def test_app_loads_a_config_module(self):
        assert False

    def test_app_loads_default_dev_config_if_no_one_was_passed(self):
        assert False

    def test_home_route_returns_status_code_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_route_should_render_search_form(self):
        assert False

    def test_post_for_home_route_returns_a_bad_request_without_machine_parameter(self):
        response = self.client.post('/')
        self.assertEqual(response.status_code, 400)

    @mock.patch('requests.get')
    def test_search_for_machine_should_render_a_list(self, get_mock):
        get_mock.return_value.json.return_value = {
            "machine": "m",
            "vms": ["m_vm_01", "m_vm_02"]
        }
        response = self.client.post('/', data={"machine": "m"})

        assert False

    @mock.patch('requests.get')
    def test_main_input_text_has_its_value_filled_after_a_search(self, get_mock):
        assert False

    def test_returns_bad_request_validation_error_with_a_long_input_query(self):
        # Let's limmit this field to 100 chars
        string = 'a' * 110
        response = self.client.get(f'/{self.api}/{string}')
        self.assertEqual(response.status_code, 400)
