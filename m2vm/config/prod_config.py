import os


ENV = 'production'
DEBUG = os.getenv('APP_DEBUG', False)
TESTING = False
SECRET_KEY = os.getenv('APP_SECRET_KEY')
GLOBOMAP_API_URL = os.getenv('GLOBOMAP_API_URL')
