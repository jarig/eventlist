import sys
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

if os.environ['REST_BASE_PATH'] not in sys.path:
    sys.path.append(os.environ['REST_BASE_PATH'])

if os.environ['REST_APP_PATH'] not in sys.path:
    sys.path.append(os.environ['REST_APP_PATH'])

sys.path.append(os.path.join(os.environ['REST_BASE_PATH'],"_ext"))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
