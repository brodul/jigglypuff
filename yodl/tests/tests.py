import os.path
from mock import patch
import unittest2
from pyramid import testing


from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from yodl.models import Base as Entity
from yodl.models import DBSession as Session
from yodl.tests import (
    INTERNET,
    TRAVIS
)

__here__ = os.path.dirname(os.path.realpath(__file__))


class FunctionalTestCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        # http://www.sontek.net/blog/2011/12/01/writing_tests_for_pyramid_and_sqlalchemy.html
        import meta_admin
        import tempfile
        import os.path
        cls.tmpdir = tempfile.mkdtemp()

        dbpath = os.path.join(cls.tmpdir, 'test.db')
        uri = 'sqlite:///' + dbpath
        settings = {
            'sqlalchemy.url': uri,
            'pyramid.includes': []
        }
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')

        cls.Session = sessionmaker()

        cls.app = meta_admin.main({}, **settings)

    @classmethod
    def tearDownClass(cls):
        import shutil
        shutil.rmtree(cls.tmpdir)

    def setUp(self):
        from webtest import TestApp
        self.testapp = TestApp(self.app)

        connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = connection.begin()

        # bind an individual Session to the connection
        Session.configure(bind=connection)
        self.session = self.Session(bind=connection)
        Entity.session = self.session

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()


# TODO XXX
class ViewTests(unittest2.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):  # pragma: no cover
        return
        from .views import main_view
        request = testing.DummyRequest()
        info = main_view(request)
        del info


class TasksTests(unittest2.TestCase):
    from mock import mock_open
    with open(os.path.join(__here__, "fixtures/json/test.info.json")) as f:
        m = mock_open(read_data=f.read())

    @patch('__builtin__.open', m, create=True)
    @patch('yodl.tasks.add_song_to_db')
    @patch('yodl.tasks.check_song_existence')
    @patch('youtube_dl._real_main')
    def test_transcode(self, mock_main, mock_check_song, mock_add_song):
        from yodl.tasks import transcode

        self.assertEqual(
            transcode("http://www.youtube.com/watch?v=id98765", '.'),
            'f8213f97babd3a452d8196b539cf65f2'
        )
