import os
import requests
from flask import Flask, request, render_template


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
        from flask import current_app as app
        gmap_api_url = app.config.get('GLOBOMAP_API_URL')

        machine = request.form.get('machine')
        if not machine:
            return 'Missing parameter: machine', 400

        req = requests.get(f'{gmap_api_url}/{machine}')
        context = req.json()

        return render_template('search.html', **context)


    @app.route('/dummy-gmap-api/<string:machine>', methods=['GET'])
    def dummy_gmap_api(machine):
        return {
            'machine': machine,
            'vms': [{'name': f'{machine}_vm_{n:02}',
                     'ip': f'10.0.0.{n}'} for n in range(1, 11)]
        }


    return app
