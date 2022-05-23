#  file: backend/settings/develop.py

from .base import *
from config import db_config, django_config

SECRET_KEY = django_config["SECRET_KEY"]
DEBUG = True
ALLOWED_HOSTS = ['*'] # blank means 'localhost', '127.0.0.1'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oruum_db',
        'USER': 'root',
        'PASSWORD': db_config["password"],
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}