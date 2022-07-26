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
ALLOWED_HOSTS = ['oruum', 'localhost', 'web', '127.0.0.1', '3.37.170.52', '0.0.0.0']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  secrets["db_config"]["schema"],
        'USER': secrets["db_config"]["user"],
        'PASSWORD': secrets["db_config"]["password"],
        'HOST': 'oruum-mysql', # 'localhost'
        'PORT': '3306',
    }
}
