import random
import string

from cornice import Service
from cornice.resource import resource

transcode = Service(
    name='transcode',
    path='/transcode',
    description="Add a song to board"
)


@transcode.post()
def post_transcode(request):
    """Returns a list of all boards."""
    # get id
    # get name
    ''.join(
        random.choice(string.ascii_lowercase + string.digits)
        for _ in range(16)
    )
    # transcode
    # save as the salted name
    # add to songs (internally)
    # add to board with the relation to songs (internally)
    return {'boards': ['main']}


@resource(collection_path='/boards', path='/boards/{id}')
class board(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        """Returns a list of all boards."""
        return {'boards': ['main']}

    def get(self):
        return {'id': 1,
                'name': 'main',
                'owner': ['Authenticated'],
                'songs': []
                }


@resource(collection_path='/songs', path='/songs/{id}')
class songs(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        return {'songs': songs_q}

    def get(self):
        return {'id': 1,
                'videoid': '11char',
                'title': 'main',
                'lenght': '100',
                }
