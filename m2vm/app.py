import os
from flask import Flask, render_template


def create_app(config_module=None):
    app = Flask(__name__)
    app.secret_key = os.getenv('APP_SECRET_KEY', '4pp53cr37k31')
    app.config.from_object(config_module or
                           os.getenv('APP_CONFIG') or
                           'm2vm.config')


    @app.route('/', methods=['GET'])
    def index():
        return render_template('search.html')


    @app.route('/dummy-gmap-api/<string:m>', methods=['GET'])
    def dummy_gmap_api(m):
        return { 'real': m }


    return app
