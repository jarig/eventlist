# Django settings for Rest project.
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test',                      # Or path to database file if using sqlite3.
        'USER': 'admin',                      # Not used with sqlite3.
        'PASSWORD': 'eiYaek5Aug',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

REST_BASE_PATH = os.environ["REST_BASE_PATH"]
REST_APP_PATH = os.environ["REST_APP_PATH"]

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(REST_BASE_PATH,'media')
STATIC_ROOT = os.path.join(REST_BASE_PATH,'static')


ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = ()

TEMPLATE_DIRS = (
    os.path.join(REST_APP_PATH, 'templates'),
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
