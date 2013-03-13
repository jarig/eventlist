from unittest import TestCase
from _ext.foursquare import settings
from _ext.foursquare.models import Foursquare

class SimpleTest(TestCase):
    def setUp(self):
        self.api = Foursquare(
            client_id=settings.CLIENT_ID,
            client_secret=settings.CLIENT_SECRET
        )
        self.testVenueId = "4b51ca4ef964a520ac5527e3"
        pass

    def testGetVenueInfo(self):
        response = self.api.venues(self.testVenueId)
        print response["venue"]["name"]
        pass
