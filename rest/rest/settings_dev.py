# Django settings for Rest project.
import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'eventlist',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'q1w2e3',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}


INTERNAL_IPS = ('127.0.0.1',
                'localhost',)
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ROOT_PATH = os.path.abspath(".")
MEDIA_ROOT = os.path.abspath(".")+'/media/'
STATIC_ROOT = os.path.abspath(".")+'/static/'

SOLR_DISTRIB = "E:\\Apps\\solr-4.3.1\\example"
SOLR_HOME = os.path.join(ROOT_PATH, "../solr")

sys.path.append(os.path.join(ROOT_PATH, "_ext"))

ADMIN_MEDIA_PREFIX = '/static/admin/'

TEMPLATE_DIRS = (
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(".")+'/templates',
)

CACHES = {
    #TODO: use memcached
    'longMem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    },
    'shortMem': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'eden'
    },
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
