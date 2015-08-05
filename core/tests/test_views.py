__author__ = 'vitor'

from django.test import TestCase
from django.core.urlresolvers import reverse as r

class RestViewGetTest(TestCase):

    def setUp(self):
        self.resp = self.client.get(r('person'))

    def test_get(self):
        #get / deve retornar status code 200
        self.assertEqual(200, self.resp.status_code)

