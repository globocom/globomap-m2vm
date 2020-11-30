import logging
from datetime import datetime
import requests
from flask import current_app, session

log = logging.getLogger(__name__)


class GmapClient:

    def __init__(self):
        self.gmap_api_url = current_app.config.get('GLOBOMAP_API_URL')
        self.username = current_app.config.get('GLOBOMAP_API_USERNAME')
        self.password = current_app.config.get('GLOBOMAP_API_PASSWORD')
        self.token_data = None
        self.auth()

    def auth(self):
        if session.get('token_data'):
            expires = datetime.strptime(session['token_data']['expires_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if expires > datetime.now():
                self.token_data = session['token_data']
                return

        try:
            token_data = requests.post(f'{self.gmap_api_url}/auth/', json={
                'username': self.username,
                'password': self.password
            }).json()
            session['token_data'] = token_data
            self.token_data = token_data
        except Exception as err:
            log.exception(f'Globomap API auth error: {err}')

    def find_nodes(self, server_name):
        req = requests.get(f'{self.gmap_api_url}/collections/search/',
                           params={'query': f'[[{{"field":"name","operator":"LIKE","value":"{server_name}"}}], \
                                               [{{"field":"properties.equipment_type", "operator":"==", "value":"Servidor"}}]]',
                                   'collections': ['comp_unit']},
                           headers={'Authorization': self.token_data.get('token')})
        return req.json()

    def find_vms(self, physical_id):
        req = requests.get(f'{self.gmap_api_url}/graphs/physical_host/traversal/',
                           params={'graph' : 'physical_host',
                                   'start_vertex' : physical_id,
                                   'max_depth' : '1',
                                   'direction': 'any',
                                   'collections': ['comp_unit']},
                           headers={'Authorization': self.token_data.get('token')})
        return req.json()
