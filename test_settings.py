from os.path import expanduser

from foundry.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'jmbo_twitter',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.gis',
    'atlas',
    'category',
    'jmbo',
    'photologue',
    'secretballot',
    'publisher',
    'south',
]

USE_TZ = True

SITE_ID = 1

CKEDITOR_UPLOAD_PATH = expanduser('~')

# Disable celery
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'

SOUTH_TESTS_MIGRATE = False
