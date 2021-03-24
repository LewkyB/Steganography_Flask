import unittest

from irctube import app


class TestViews(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index(self):
        rv = self.client.get('/')
        self.assertEqual(rv.status_code, 200)
