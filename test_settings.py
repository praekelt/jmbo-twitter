from os.path import expanduser

from foundry.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_jmbo_twitter',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CKEDITOR_UPLOAD_PATH = expanduser('~')

# Disable celery
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = 'memory'
