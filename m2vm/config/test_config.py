import os


ENV = 'testing'
DEBUG = True
TESTING = True
SECRET_KEY = os.getenv('APP_SECRET_KEY', '4pp53cr37k31')
GLOBOMAP_API_URL = os.getenv('GLOBOMAP_API_URL',
                             'http://localhost:8888/dummy-gmap-api')
GLOBOMAP_API_USERNAME = os.getenv('GLOBOMAP_API_USERNAME', 'username')
GLOBOMAP_API_PASSWORD = os.getenv('GLOBOMAP_API_PASSWORD', 'password')

