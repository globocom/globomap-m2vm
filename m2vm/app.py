import os
from flask import Flask, request, render_template, redirect
import requests

def create_app(config_module=None):
    app = Flask(__name__)
    app.secret_key = os.getenv('APP_SECRET_KEY', '4pp53cr37k31')
    app.config.from_object(config_module or
                           os.getenv('APP_CONFIG') or
                           'm2vm.config')


    @app.route('/', methods=['GET', 'POST'])
    def index():
        machine = request.form.get('machine')
        context = {}
        if machine:
            print (machine)
            r = requests.get('http://localhost:8888/dummy-gmap-api/' + machine)
            context[machine] = r.json().get('machine')

        return render_template('search.html', info=context)

    @app.route('/dummy-gmap-api/<string:m>', methods=['GET'])
    def dummy_gmap_api(m):
        return { 'machine': {'vm1': 'vm' + m} }


    return app
