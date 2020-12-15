import os
import json
import logging
from flask import Flask, request, render_template, url_for, redirect
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
        search_type = request.form.get('search_type', 'by_name')
        server_q = request.form.get('server_q')

        if not server_q:
            return 'Missing parameter: name or ip', 400

        if search_type == 'by_name' and len(server_q) > 100:
            return 'Name is too long (max of 100 chars)', 400

        query = 'query_physical_servers'
        if search_type == 'by_ip':
            query = 'query_physical_servers_by_ip'

        status, data = GmapClient().run_query(query, server_q)

        if status > 399:
            return data, status

        context = {
            'search_type': search_type,
            'server_q': server_q,
            'server_list': [],
            'step': 1
        }

        if len(data):
            for item in data:
                vm_list_url = f"{url_for('vm_list', server_name=item['name'])}?server_id={item['_id']}"
                context['server_list'].append({
                    '_id': item['_id'],
                    'name': item['name'],
                    'ips': item['properties'].get('ips', ''),
                    'vm_list_url': vm_list_url
                })

        if len(context['server_list']) == 1:
            return redirect(context['server_list'][0]['vm_list_url'])

        return render_template('search.html', **context)

    @app.route('/<string:server_name>', methods=['GET'])
    def vm_list(server_name):
        server_id = request.args.get('server_id')
        if not server_id:
            return 'Missing parameter: server_id', 400

        status, data = GmapClient().find_vms(server_id)

        if status > 399:
            return data, status

        context = {
            'server_name': server_name,
            'vm_list': [],
            'step': 2
        }

        if len(data.get('nodes', [])):
            for item in data['nodes']:
                if item['properties'].get('equipment_type') == 'Servidor Virtual':
                    context['vm_list'].append({
                        '_id': item['_id'],
                        'name': item['name'],
                        'ips': item['properties'].get('ips', '')
                    })

        return render_template('search.html', **context)

    return app
