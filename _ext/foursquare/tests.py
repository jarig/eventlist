from unittest import TestCase

class SimpleTest(TestCase):
    def setUpClass(self):
        self.testVenueId = "40a55d80f964a52020f31ee3"
        pass

    def testGetVenueTips(self):
        self.assertEqual(1 + 1, 2)
