from subprocess import call
import sys

from django.core.management.base import BaseCommand

from rest import settings


class Command(BaseCommand):
    help = 'Create Schema Migrations for all apps'

    def _is_project_app(self, app_name):
        return not 'django' in app_name and not 'south' in app_name

    def handle(self, *args, **options):
        try:
            call([sys.executable, './manage.py', 'syncdb'])
            for app in settings.INSTALLED_APPS:
                if self._is_project_app(app):
                    print "Creating migration for " + app
                    call([sys.executable,'./manage.py', 'schemamigration', app,'--auto'])

            print 'All applications migrated.'
        except Exception as e:
            print e
            pass

  