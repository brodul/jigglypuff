import logging
import socket

from cornice import Service
from cornice.resource import resource

from jigglypuff.tasks import main_task
from jigglypuff.models import Song
from jigglypuff.models import Board
from jigglypuff.models import DBSession
from jigglypuff.celery_utils import celery

log = logging.getLogger(__name__)


class ErrorMixin(object):
    def client_error(self, msg):
        self.request.response.status_code = 400
        return {'error': True, 'error_msg': msg}


status = Service(
    name='status',
    path='/status',
    description="Get status"
)


@status.get()
def get_status(request):
    i = celery.control.inspect(timeout=0.1)
    try:
        wa = isinstance(i.stats(), dict)
        active = i.active()
        queue = i.scheduled()
    except socket.error:
        log.error("Could not connect to RabbitMQ server.")
        raise
    return {
        'wa': wa,
        'active': active,
        'queue': queue,
    }


transcode = Service(
    name='transcode',
    path='/transcode',
    description="Add a song to board"
)


@resource(collection_path='/trans', path='/trans/{id}')
class transcode(ErrorMixin, object):

    def __init__(self, request):
        self.request = request

    def collection_post(self):
        # DRY
        url = self.request.json_body.get('url')
        if url is None:
            return self.client_error('No JSON key "url"')
        url = url.strip()

        board = self.request.json_body.get("board")
        if board is None:
            return self.client_error('No JSON key "board"')
        board = board.strip()

        # check if id and file all ready exists
        if board != 'main':
            self.request.response.status_code = 400
            return {'error': True, 'error_msg': 'Invalid board.'}
        main_task.s(
            url,
            media_path=self.request.registry.settings['jigglypuff.media_path']
        ).apply_async()
        # get id
        # get name
        # transcode
        # save as the salted name
        # add to songs (internally)
        # add to board with the relation to songs (internally)
        return {'boards': ['main']}


@resource(collection_path='/boards', path='/boards/{id}')
class board(ErrorMixin, object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        """Returns a list of all boards."""
        return {"boards": {1: "main"}}
        # XXX
        boards = dict((board.id, board.name) for board in DBSession.query(Board).all())
        return {'boards': boards}

    def get(self):
        return {
            "id": 1,
            "name": "main",
            "songs": dict((song.id, song.get_dict()) for song in DBSession.query(Song).all())
        }
        board = DBSession.query(Board).all()
        board_d = board.get_dict()
        return {'name': board_d['name'],
                'owner': {1: 'Authenticated'},
                'songs': board_d['songs']
                }


@resource(collection_path='/songs', path='/songs/{id}')
class songs(ErrorMixin, object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        songs = dict((song.id, song.file_id) for song in DBSession.query(Song).all())
        return {'songs': songs}

    def get(self):
        song = DBSession.query(Song).get(int(self.request.matchdict['id']))
        return song and song.get_dict() or {}
