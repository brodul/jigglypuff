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

from yodl.celery_utils import celery
from yodl.models import SongItem


Task_DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension())
)
engine = create_engine('sqlite:///file.db')
Task_DBSession.configure(bind=engine)


@celery.task
def transcode(url, media_path, audio_format=None):
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

    if (file_id, ) in Task_DBSession.query(SongItem.file_id).all():
        return

    try:
        call_youtube_dl(args)
    except SystemExit as e:
        if not e.code is None:
            raise


    with open('%s.info.json' % raw_file) as f:
        parsed_json = json.load(f)

    task = SongItem(
        songname=parsed_json['title'],
        youtube_id=parsed_json['id'],
        file_id=file_id
    )
    Task_DBSession.add(task)
    transaction.commit()

    return file_id
