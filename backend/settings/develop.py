#  file: backend/settings/develop.py

from .base import *
import os
import json
config_file = os.path.join(BASE_DIR, 'config.json')
with open(config_file) as f:
    secrets = json.loads(f.read())

SECRET_KEY = secrets["django_config"]["SECRET_KEY"]
DEBUG = True
# blank means 'localhost', '127.0.0.1'
ALLOWED_HOSTS = ['localhost', 'oruum-api-server', 'api.oruum.com', '3.37.170.52', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  secrets["db_config"]["schema"],
        'USER': secrets["db_config"]["user"],
        'PASSWORD': secrets["db_config"]["password"],
        'HOST': 'localhost', # if run in local, HoST is 'localhost'
        # 'HOST': 'oruum-mysql', # if using, docker-compose
        'PORT': '3306',
    }
}
