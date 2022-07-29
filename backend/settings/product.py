#  file: backend/settings/product.py

from .base import *
import os
import json
config_file = os.path.join(BASE_DIR, 'config.json')
with open(config_file) as f:
    secrets = json.loads(f.read())

SECRET_KEY = secrets["django_config"]["SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ['api2.oruum.com', '3.37.170.52', 'oruum-api-server']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  secrets["db_config"]["schema"],
        'USER': secrets["db_config"]["user"],
        'PASSWORD': secrets["db_config"]["password"],
        'HOST': 'oruum-mysql', 
        'PORT': '3306',
    }
}