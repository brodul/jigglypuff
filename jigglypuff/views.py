from urlparse import urlparse
from urlparse import parse_qs
import logging
import socket

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from jigglypuff.tasks import transcode
from jigglypuff.models import SongItem
from jigglypuff.models import DBSession
from jigglypuff.celery_utils import celery


log = logging.getLogger(__name__)


def url_validate(url):
    """docstring for url_validate"""
    o = urlparse(url)
    try:
        query = parse_qs(o.query)
        if o.netloc.endswith("youtube.com")\
                and query.keys() == [u'v']:
            return url
    except:
        pass


@view_config(route_name='home', renderer='templates/index.jinja2')
def main_view(request):
    if request.POST:
        url = request.params["url"].strip()
        # check if id and file all ready exists
        if url_validate(url):
            transcode.delay(
                url,
                media_path=request.registry.settings['jigglypuff.media_path']
            )
            request.session["error"] = False

        else:
            request.session["error"] = True

        return HTTPFound(request.route_url('home'))
    i = celery.control.inspect(timeout=0.05)
    try:
        wa = isinstance(i.stats(), dict)
        active = i.active()
        queue = i.scheduled()
    except socket.error:
        log.error("Could not connect to RabbitMQ server.")
        raise

    songs = DBSession.query(SongItem).all()
    return {
        'songs': songs,
        'queue': queue,
        'active': active,
        'workers_available': wa,
    }
