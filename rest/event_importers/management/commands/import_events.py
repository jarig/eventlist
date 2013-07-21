import datetime
from django.core.management.base import BaseCommand
from django.core.cache import cache
from event_importers.models import SuperKinodSource


class Command(BaseCommand):
    help = 'Imports events from different sources'

    def handle(self, *args, **kwargs):
        #import Forum-cinemas movies
        superKinodSource = SuperKinodSource()
        imported = superKinodSource.importEvents(datetime.date.today() + datetime.timedelta(days=1))
        print "Events imported: %s" % len(imported)
        pass
