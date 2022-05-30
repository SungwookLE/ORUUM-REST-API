#  file: backend/settings/product.py

from .base import *
import os
import json

config_file = os.path.join(BASE_DIR, 'config.json') 
with open(config_file) as f:
    secrets = json.loads(f.read())

SECRET_KEY = secrets["django_config"]["SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secrets["db_config"]["schema"],
        'USER': secrets["db_config"]["user"],
        'PASSWORD': secrets["db_config"]["password"],
        'HOST': 'localhost',  # 수정해야함 배포시('22.4/7)
        'PORT': '3306',
    }
}
