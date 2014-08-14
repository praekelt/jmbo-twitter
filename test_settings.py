DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': 'jmbo-twitter.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS = [
    'jmbo_twitter',
    'foundry',
    'jmbo',
    'photologue',
    'category',
    'secretballot',
    'publisher',
    'preferences',
    'atlas',
    'south',
    'django.contrib.auth',
    'django.contrib.comments',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.gis',
]

SITE_ID = 1
STATIC_URL = '/'
SOUTH_TESTS_MIGRATE = False
