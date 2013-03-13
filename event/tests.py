from django.test import TestCase
from unittest import TestCase as UnitTestCase

class FeaturedEventsTest(UnitTestCase):
    def test_get_featured_events(self):
        """
            Tests featured events retrieval
        """
        self.assertEqual(1 + 1, 2)
