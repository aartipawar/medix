from .base import *
import os,sys

DEBUG = True

ALLOWED_HOSTS = ['*']

# DATABASES = {
#     'default': {
#         'ENGINE':   'django.db.backends.postgresql',
#         'NAME':     'medix',
#         'USER':     'postgres',
#         'PASSWORD': 'psql',
#         'HOST':     'localhost',
#         'PORT':     5432,
#     }
# }

STATIC_URL = '/static/'
STATIC_ROOT = PROJECT_DIR.child("collected_static")
STATICFILES_DIRS = (
    PROJECT_APPS.child("static"),
)

MEDIA_ROOT = PROJECT_APPS.child("media")
MEDIA_URL = '/media/'



ROOT_URL = "http://18.218.141.80"