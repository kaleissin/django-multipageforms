from .base import *

DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MIDDLEWARE_CLASSES = ()

INSTALLED_APPS += ['multipageforms.tests']

SECRET_KEY = 'na2Tei0FoChe3ooloh5Yaec0ji7Aipho'

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_PATTERN = "*"

