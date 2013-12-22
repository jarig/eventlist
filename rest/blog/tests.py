"""

"""
import json

from unittest import TestCase
from blog import utils
from blog.utils import REGIONS


class UtilsTest(TestCase):

    def test_grad_conversion(self):
        """
            Test coordinate conversion
        """
        gradToConvert = 23.48
        decToConvert = 23.80
        dec = utils.gradToDec(gradToConvert)
        grad = utils.decToGrad(decToConvert)
        self.assertTrue(dec == decToConvert and grad == gradToConvert)

    def test_retrieve_venues_from_region(self):
        """
            Test venue data export from foursquare
        """
        #ne=59.536407,25.084877&sw=59.336691,24.528008
        result = utils.getFourSquareVenues(REGIONS["Country"]["Tallinn"])
        open("venues.txt","w").write(json.dumps(result, indent=2))
        self.assertTrue(type(result) == dict)
        self.assertTrue(result.has_key("venues"))
        self.assertTrue(len(result["venues"]) > 0)
        print len(result["venues"])

