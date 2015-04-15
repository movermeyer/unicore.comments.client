from unittest import TestCase
from uuid import uuid4

import responses

from unicore.comments.client.base import BaseClient


class BaseClientTestMixin(object):

    @classmethod
    def setUpClass(cls):
        cls.app_id = uuid4().hex
        cls.host = 'http://localhost:8000'
        cls.client = cls.client_class(host=cls.host)

    def check_request_basics(self, url):
        self.assertEqual(len(responses.calls), 1)
        request = responses.calls[0].request
        self.assertEqual(request.url, url)

    def test_from_config(self):
        settings = {
            'unicorecomments.host': 'http://localhost:8080',
        }
        client = self.client_class.from_config(settings)
        self.assertEqual(client.settings, {
            'host': settings['unicorecomments.host']})


class BaseClientTestCase(TestCase, BaseClientTestMixin):
    client_class = BaseClient
