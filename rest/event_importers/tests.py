"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from unittest import TestCase
import datetime
from event_importers.models import SuperKinodSource


class ImportTest(TestCase):

    def test_source_superkinod(self):
        """
        Tests that events from superkinod.ee can be imported
        """
        source = SuperKinodSource()
        events = source.importEvents(datetime.date.today() + datetime.timedelta(days=1))
        self.assertTrue(len(events)> 0)
        for event in events:
            self.assertTrue(len(event.name) > 0)  # every event should have name
            print event.name
            print event.descr
            print event.logo
            print event.activities.all()
            print event.schedules.all()

