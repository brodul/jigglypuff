import hashlib
import os
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension
from youtube_dl import _real_main as call_youtube_dl
import transaction

from jigglypuff.celery_utils import celery
from jigglypuff.models import SongItem


Task_DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension())
)
engine = create_engine('sqlite:///file.db')
Task_DBSession.configure(bind=engine)


def check_song_existence(file_id):
    """@todo: Docstring for check_song_existence.

    :file_id: @todo
    :returns: @todo

    """
    if (file_id, ) in Task_DBSession.query(SongItem.file_id).all():
        return False
    else:
        return True


def add_song_to_db(file_id, parsed_json):
    """@todo: Docstring for add_song_to_db.

    :arg1: @todo
    :returns: @todo

    """
    task = SongItem(
        songname=parsed_json['title'],
        youtube_id=parsed_json['id'],
        file_id=file_id
    )
    Task_DBSession.add(task)
    transaction.commit()


@celery.task
def transcode(url, media_path, audio_format=None, Task_DBSession=Task_DBSession):
    """docstring for dl_transcode"""
    audio_format = audio_format or 'vorbis'
    user_agent = 'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/534.57.2\
 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'

    file_id = hashlib.md5(url).hexdigest()
    raw_file = os.path.join(media_path, file_id)
    args = [
        '-k',
        '--extract-audio',
        '--audio-format', audio_format,
        '--audio-quality', '0',
        '--user-agent', user_agent,
        '--no-progress',
        '--write-info-json',

        '--output', raw_file + '.%(ext)s',

        url
    ]

    check_song_existence(file_id)

    try:
        call_youtube_dl(args)
    except SystemExit as e:
        if not e.code is None:
            raise

    with open('%s.info.json' % raw_file) as f:
        parsed_json = json.load(f)

    add_song_to_db(file_id, parsed_json)

    return file_id
