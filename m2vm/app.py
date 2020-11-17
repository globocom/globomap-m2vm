import os
from flask import Flask


def create_app(config_module=None):
    app = Flask(__name__)
    app.secret_key = os.getenv('APP_SECRET_KEY', '4pp53cr37k31')
    app.config.from_object(config_module or
                           os.getenv('APP_CONFIG') or
                           'm2vm.config')
    return app
