#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", content))
    return metadata['version']

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_mako',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'pyramid_raven',
    'waitress',
    'sqlalchemy',
    'celery',
    'zope.sqlalchemy',
    'mock',
    'nose',
    'unittest2',
    'webtest',
    'raven',
    'cornice',
    'alembic',
    'gunicorn',
    'pafy==0.3.76',
]

setup(name='jigglypuff',
      version=get_version('jigglypuff/__init__.py'),
      description='jigglypuff',
      long_description=readme + '\n\n' + history,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      keywords='web pyramid pylons',
      packages=find_packages(exclude=['supervisor', 'tests', 'tests.*']),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite='nose.collector',
      entry_points={
          b'paste.app_factory': [
              'main = jigglypuff:main',
          ],
          'console_scripts': [
              'jigglypuffstart = jigglypuff.scripts.gunicorn_wrapper:main',
              'celery = celery.__main__:main',
          ]
      },
      )
