"""
See this:
https://hynek.me/articles/using-celery-with-pyramid/
"""
import os

from pyramid.paster import bootstrap
from celery import Celery


celery = Celery('proj.celery',
                broker='amqp://',
                backend='amqp://',
                include=['yodl.tasks'])

# Optional configuration, see the application user guide.
celery.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    celery.start()

#celery.config_from_object('celeryconfig')
