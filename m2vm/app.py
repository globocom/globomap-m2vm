import os
import json
import logging
import requests

from flask import Flask, current_app, request, render_template

log = logging.getLogger(__name__)


class GmapClient:

    def __init__(self):
        self.gmap_api_url = current_app.config.get('GLOBOMAP_API_URL')
        self.username = current_app.config.get('GLOBOMAP_API_USERNAME')
        self.password = current_app.config.get('GLOBOMAP_API_PASSWORD')
        self.token_data = None
        self.auth()

    def auth(self):
        try:
            self.token_data = requests.post(f'{self.gmap_api_url}/auth/', json={
                'username': self.username,
                'password': self.password
            }).json()
        except Exception as err:
            log.exception(f'Globomap API auth error: {err}')

    def find_nodes(self, q_var):
        req = requests.get(f'{self.gmap_api_url}/collections/search/',
                           params={
                               'query': f'[[{{"field":"name","operator":"LIKE","value":"{q_var}"}}]]' ,
                               'collections': ['comp_unit']
                           },
                           headers={'Authorization': self.token_data.get('token')})
        return req.json()


def create_app(config_module=None):
    app = Flask(__name__)

    if config_module:
        app.config.from_pyfile(config_module)
    else:
        app.config.from_pyfile('config/dev_config.py')

    @app.route('/', methods=['GET'])
    def home():
        return render_template('search.html')

    @app.route('/', methods=['POST'])
    def vm_list():
        machine = request.form.get('machine')

        if not machine:
            return 'Missing parameter: machine', 400

        if len(machine) > 100:
            return 'Input is too long (max of 100 chars)', 400

        gmap_client = GmapClient()
        data = gmap_client.find_nodes(machine)

        context = {}

        return render_template('search.html', **context)

    return app
