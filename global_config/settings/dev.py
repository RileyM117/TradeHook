from .common import *


DEBUG = True

SECRET_KEY = 'django-insecure-8sc_r(ai(fy0yt_z8+=(k%+6m6u^pi+y4-az#nh^k4q+^r&7r+'

if DEBUG:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'trader',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'Ripoop117!'
    }
}