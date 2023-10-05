from .common import *
import os


DEBUG = False

SECRET_KEY = os.environ['SECRET_KEY']

if DEBUG:
    MIDDLEWARE += ['silk.middleware.SilkyMiddleware']

ALLOWED_HOSTS = []

