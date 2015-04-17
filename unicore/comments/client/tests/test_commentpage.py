from unittest import TestCase

import mock

from unicore.comments.client.tests import fixtures as f
from unicore.comments.client import CommentPage, CommentClient, Comment


class CommentPageTestCase(TestCase):

    def setUp(self):
        self.client = mock.Mock(spec=CommentClient)
        self.page = CommentPage(self.client, f.comment_stream_data)

    def test_properties(self):
        self.assertEqual(self.page.start, f.comment_stream_data['start'])
        self.assertEqual(self.page.end, f.comment_stream_data['end'])
        self.assertEqual(self.page.total, f.comment_stream_data['total'])
        self.assertEqual(self.page.metadata, f.comment_stream_data['metadata'])
        self.assertEqual(
            self.page.state, f.comment_stream_data['metadata']['state'])

    def test_iterable(self):
        length = len(self.page)
        self.assertEqual(length, f.comment_stream_data['count'])

        for i, comment in enumerate(self.page):
            self.assertIsInstance(comment, Comment)
        self.assertEqual(i, length - 1)
