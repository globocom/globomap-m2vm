import os


ENV = 'development'
DEBUG = True
TESTING = False
SECRET_KEY = os.getenv('APP_SECRET_KEY', '4pp53cr37k31')
GLOBOMAP_API_URL = os.getenv('GLOBOMAP_API_URL',
                             'http://localhost:8888/dummy-gmap-api')
