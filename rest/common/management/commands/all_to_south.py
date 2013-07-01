from subprocess import call
import sys

from django.core.management.base import BaseCommand

from rest import settings


class Command(BaseCommand):
    help = 'Convert all apps to south'
    
    def _is_project_app(self, app_name):
        return not 'django' in app_name and not 'south' in app_name

    def handle(self, *args, **options):
        try:
            call([sys.executable, './manage.py', 'syncdb'])

            for app in settings.INSTALLED_APPS:
                if self._is_project_app(app):
                    print "Converting " + app
                    call([sys.executable,'./manage.py', 'convert_to_south', app])

            print 'All applications converted to south'
        except Exception as e:
            print e
            pass
