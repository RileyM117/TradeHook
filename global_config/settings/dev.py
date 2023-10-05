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

CELERY_BROKER_URL = 'redis://localhost:6379/1'
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://@localhost:6379/2",
        'TIMEOUT': 10 * 60,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 2525