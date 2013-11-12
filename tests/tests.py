import unittest

from mock import patch
from pyramid import testing

from yodl.tests import (
    INTRANET,
    TRAVIS
)


class ViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        return
        from .views import main_view
        request = testing.DummyRequest()
        info = main_view(request)


class TaskTests(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_get_id(self, mock_popen):
        from yodl.tasks import get_id
        mock_popen.return_value.communicate.return_value = \
            ('id98765', '')
        mock_popen.return_value.returncode = 0

        self.assertEqual(
            get_id("http://www.youtube.com/watch?v=id98765"),
            'id98765'
        )

    @unittest.skipUnless(*INTERNET)
    @unittest.skipUnless(*TRAVIS)
    def test_get_id_implement(self):
        from yodl.tasks import get_id

        self.assertEqual(
            get_id("http://www.youtube.com/watch?v=c5NL76BXauY"),
            'c5NL76BXauY'
        )
