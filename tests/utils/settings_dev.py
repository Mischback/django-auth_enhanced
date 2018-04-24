# -*- coding: utf-8 -*-
"""Contains minimum settings to run the development inside of
tox-environments and run the tests.

Please note, that some settings are explicitly set by the testrunner (see
runtests.py), i.e. migrations will be disabled by default during tests."""

# Python imports
import sys
from os.path import abspath, dirname, join, normpath

# path to the tests directory
TEST_ROOT = dirname(dirname(abspath(__file__)))

# path to the project directory
PROJECT_ROOT = dirname(TEST_ROOT)

# add PROJECT_ROOT to Python path
sys.path.append(normpath(PROJECT_ROOT))

# enable debugging (will be set to False by running tests)
DEBUG = True

# allow all hosts (will be set to [] by running tests)
ALLOWED_HOSTS = ['*']

# database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': join(TEST_ROOT, 'test.sqlite'),
    }
}

# minimum installed apps to make the app work
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',   # introduced to make the admin usable inside tox
    'auth_enhanced.apps.AuthEnhancedConfig'
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [join(TEST_ROOT, 'utils', 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                # 'django.template.context_processors.i18n',
                # 'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# we need a development/test specific url configuration
ROOT_URLCONF = 'tests.utils.urls_dev'

# provide a static URL for development
# introduced to make the admin usable inside tox
STATIC_URL = '/static/'

# this is a minimum test requirement
SECRET_KEY = 'only-for-testing'

# adjust Django's default setting to this app's login view
#   Django's default: '/accounts/login/'
LOGIN_URL = 'auth_enhaced:login'

# if there is no special next parameter after login, show this page
#   Django's default: '/accounts/profile/'
LOGIN_REDIRECT_URL = '/'
