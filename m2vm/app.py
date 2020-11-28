import os
import json
import logging
from flask import Flask, request, render_template
from .client import GmapClient

log = logging.getLogger(__name__)


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
    def server_list():
        server_name = request.form.get('server_name')

        if not server_name:
            return 'Missing parameter: server_name', 400

        if len(server_name) > 100:
            return 'Input is too long (max of 100 chars)', 400

        context = {'server_name': server_name, 'server_list': []}
        data = GmapClient().find_nodes(server_name)

        if len(data['documents']):
            for item in data['documents']:
                context['server_list'].append({
                    '_id': item['_id'],
                    'name': item['name'],
                    'ips': item['properties'].get('ips', '')
                })

        return render_template('search.html', **context)

    @app.route('/<string:server_name>', methods=['POST'])
    def vm_list(server_name):
        server_id = request.json.get('server_id')
        data = GmapClient().find_vms(server_id)

        vm_list = []
        for item in data['nodes']:
            if item['properties'].get('equipment_type') == 'Servidor Virtual':
                vm_list.append(item)

        return {'vm_list': vm_list}

    return app
