from .base import *


SECRET_KEY = 'django-insecure-n2hnn=ggfzp4i2(ed-$rlf_ovsdu@v9ie!3-%*g!=bs-lqhu0x'


DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oruum_db',
        'USER': 'root',
        'PASSWORD': '3102',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}