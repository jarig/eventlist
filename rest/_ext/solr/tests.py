from unittest import TestCase
from _ext import solr

class SolrSearchTest(TestCase):
    def setUp(self):
        self.solr = solr.SolrConnection("http://localhost:8983/solr/")
        pass

    def testSolrFuzzyQuery(self):
        response = self.solr.query('name:Cafi~0.7')
        for hit in response.results:
            print hit['name']
        pass

