import os.path
import unittest2
from pyramid import testing

from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from jigglypuff.models import Base as Entity
from jigglypuff.models import DBSession as Session

__here__ = os.path.dirname(os.path.realpath(__file__))


class FunctionalTestCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        # http://www.sontek.net/blog/2011/12/01/writing_tests_for_pyramid_and_sqlalchemy.html
        import jigglypuff
        import tempfile
        import os.path
        cls.tmpdir = tempfile.mkdtemp()

        dbpath = os.path.join(cls.tmpdir, 'test.db')
        uri = 'sqlite:///' + dbpath
        settings = {
            'sqlalchemy.url': uri,
            'pyramid.includes': [],
        }
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')

        cls.Session = sessionmaker()

        cls.app = jigglypuff.main({}, **settings)

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


class BoardTests(FunctionalTestCase):

    def test_title(self):
        resp = self.testapp.get('/')
        self.assertIn(u'<title>Jigglypuff</title>', resp.text)
