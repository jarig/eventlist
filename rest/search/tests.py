"""
    Test basic search functionality
"""
from datetime import datetime
import hashlib

from django.test import TestCase
from search.models import SearchRequest


class SimpleTest(TestCase):
    def test_search_request_creation(self):
        searchRequest = SearchRequest()
        searchRequest.request = "{country:'1', city:'2'}"
        searchRequest.save()
        self.assertTrue(searchRequest.token == hashlib.md5(searchRequest.request).hexdigest())
        pass

    def test_search_request_ttl(self):
        searchRequest = SearchRequest()
        searchRequest.request = "{country:'1', city:'2'}"
        searchRequest.save()
        self.assertTrue(searchRequest.ttl > datetime.now())
        pass
