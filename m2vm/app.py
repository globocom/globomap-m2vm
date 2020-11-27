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
                               'query': f'''[[{{"field":"name","operator":"LIKE","value":"{q_var}"}}, {{"field":"properties.equipment_type", "operator":"==", "value":"Servidor"}}]]''' ,
                               'collections': ['comp_unit']
                           },
                           headers={'Authorization': self.token_data.get('token')})
        return req.json()

    def find_vms(self, phys):
        req = requests.get(f'{self.gmap_api_url}/graphs/{phys.graph}/traversal/',
                            params={
                                'graph' : phys.graph,
                                'start_vertex' : 'comp_unit/globomap_cmaq24mp01lc13',#phys.id,
                                'max_depth' : '4'
                            },
                           headers={'Authorization': self.token_data.get('token')})
        return req.json()

class PhysicalMachine:
    def __init__(self, name=None, id=None):
        self.name = name
        self.id = name
        self.graph = 'physical_host'


def create_app(config_module=None):
    app = Flask(__name__, static_url_path='/static')

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

        phys = []
        #num_documents in a page
        num_documents = data['total']
        for document in range(num_documents):
            phys.append(PhysicalMachine(data['documents'][document]['name'], data['documents'][document]['_id']))

        vms = gmap_client.find_vms(phys[0])

        import ipdb; ipdb.set_trace()
        context = {'phys': phys}

        return render_template('search.html', **context)

    return app
