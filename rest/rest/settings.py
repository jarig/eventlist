# Django settings for Rest project.
import os
import sys

ADMINS = (
    ('Jaroslav', 'j.gorjatsev@gmail.com'),
)

MANAGERS = ()
ALLOWED_HOSTS = ['*', 'localhost', '127.0.0.1', 'staging.rest.ee', 'staging.rest.ee:8080']
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Tallinn'
TIME_FORMAT = 'H:i'
#DATE_FORMAT
#

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('et', 'Estonian'),
    ('ru', 'Russian'),
    ('en', 'English'),
)

LOCALE_PATHS = (
    os.path.join(os.path.dirname(__name__), "locale"),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
#USE_L10N = True

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(os.path.dirname(__name__)) + '/compiled',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fgxa6hve-u+oa&k8u)a_=n8de#-8_7+kw*8&m#oy&r2szg5zh7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #   'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
#django.contrib.sessions.backends.signed_cookies

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

AUTH_PROFILE_MODULE = 'account.Account'

AUTHENTICATION_BACKENDS = (
    'account.backends.__init__.PublicAuth',
    'account.backends.__init__.NativeAuth',
)

ROOT_URLCONF = 'rest.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.abspath(".") + '/templates',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
)
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': 'http://127.0.0.1:8983/solr'
    },
}

SOUTH_TESTS_MIGRATE = False
SOUTH_AUTO_FREEZE_APP = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'rest',
    '_ext.pibu',
    '_ext.haystack',
    'party',
    'messaging',
    'common',
    'event',
    'blog_modules',
    'blog',
    'menu',
    'account',
    'search',
    'publisher',
    'album',
    'organization',
    'widget_tweaks',
    'south',
    'event_importers'
)

USER_MAIN_VIEW = "event.views.showEventGroups"
PUBLISHER_MAIN_VIEW = "blog.views.manage"

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOG_FOLDER = os.environ.get("REST_LOG_FOLDER", "./logs")
if not os.path.exists(LOG_FOLDER):
    os.makedirs(LOG_FOLDER)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s :: %(levelname)s :: %(name)s :: %(message)s'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        },
        'rest_import_event_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FOLDER, "import_event.log"),
            'formatter': 'standard',
            'maxBytes': 1024 * 4,
            'backupCount': 3
        },
        'rest_error_log': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FOLDER, "errors.log"),
            'formatter': 'standard',
            'maxBytes': 1024 * 4,
            'backupCount': 3
        },
        'rest_debug_log': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_FOLDER, "rest.log"),
            'formatter': 'standard',
            'maxBytes': 1024 * 4,
            'backupCount': 3
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'rest':
        {
            'handlers': ['rest_error_log', 'rest_debug_log'],
            'level': 'DEBUG',
            'propagate': True
        },
        'event_importers':
        {
            'handlers': ['rest_import_event_log', 'console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
for app in INSTALLED_APPS:
    if 'django.' not in app and not LOGGING['loggers'].has_key(app):
        LOGGING['loggers'][app] = LOGGING['loggers']['rest']

if os.environ.has_key("PRODUCTION"):
    from settings_production import *
else:
    print >> sys.stdout, "Developer Mode"
    TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.debug',) + TEMPLATE_CONTEXT_PROCESSORS
    from settings_dev import *
