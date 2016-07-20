from __future__ import unicode_literals

import os
import multiprocessing
import sys

import gunicorn.app.base
from gunicorn.six import iteritems
from pyramid.paster import get_app


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, conf, options=None):
        self.options = options or {}
        self.application = get_app(conf)
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    port = os.environ.get("PORT", 8080)
    options = {
        'bind': '%s:%s' % ('127.0.0.1', port),
        'workers': number_of_workers(),
    }
    StandaloneApplication(sys.argv[1], options).run()


if __name__ == '__main__':
    main()
