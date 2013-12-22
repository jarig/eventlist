import sys
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'rest.settings'

if os.environ['REST_BASE_PATH'] not in sys.path:
    sys.path.append(os.environ['REST_BASE_PATH'])

if os.environ['REST_APP_PATH'] not in sys.path:
    sys.path.append(os.environ['REST_APP_PATH'])

sys.path.append(os.path.join(os.environ['REST_BASE_PATH'], "_ext"))

from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()


def application(environ, start_response):
    os.environ['REST_LOG_FOLDER'] = environ['REST_LOG_FOLDER']
    return _application(environ, start_response)
