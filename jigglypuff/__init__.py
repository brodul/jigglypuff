#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.0.1'

from logging import getLogger

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sqlalchemy import engine_from_config

from jigglypuff.models import DBSession
from jigglypuff.models import Base

import os


__here__ = os.path.dirname(os.path.realpath(__file__))
logger = getLogger(__file__)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)

    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')

    # set the default for entry jigglypuff.media_path
    media_path = settings.get(
        'jigglypuff.media_path',
        os.path.join(__here__, '../media')
    )
    # add os seperator to end
    media_path = \
        media_path if media_path[-1] == os.sep else media_path + os.sep
    try:
        os.mkdir(media_path)
    except OSError as e:
        logger.info("Media directory already exist.")
        logger.debug("Exception:", exc_info=True)

    settings['jigglypuff.media_path'] = media_path

    Base.metadata.create_all(engine)
    config = Configurator(
        settings=settings,
        session_factory=my_session_factory
    )
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('media', media_path, cache_max_age=3600)
    config.add_route('home', '/')
    config.include('pyramid_jinja2')
    config.include('pyramid_tm')
    config.include('cornice')
    config.scan()
    return config.make_wsgi_app()
