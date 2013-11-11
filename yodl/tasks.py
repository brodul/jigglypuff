import subprocess

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
import transaction
from zope.sqlalchemy import ZopeTransactionExtension

from yodl.celery_utils import celery
from yodl.models import SongItem


Task_DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension())
)
engine = create_engine('sqlite:///file.db')
Task_DBSession.configure(bind=engine)


@celery.task
def transcode(url):
    """docstring for dl_transcode"""
    id_ = get_id(url)

    if (id_, ) in Task_DBSession.query(SongItem.youtube_id).all():
        return
    p = subprocess.Popen(
        ["youtube-dl", url, '-x', '--audio-format', 'vorbis', '--id'],
        cwd='yodl/media/'
    )
    p.wait()
    title = get_title(url)

    task = SongItem(songname=title.strip().decode('utf8'), youtube_id=id_)
    Task_DBSession.add(task)
    transaction.commit()

    return p.returncode, id_, title


@celery.task
def get_title(url):
    """docstring for dl_get_title"""
    p = subprocess.Popen(["youtube-dl", url, '-e'], stdout=subprocess.PIPE)
    p.wait()
    title, err = p.communicate()
    title = title.strip()
    return title


@celery.task
def get_id(url):
    """docstring for get_id"""
    p = subprocess.Popen(
        ["youtube-dl", url, '--get-id'],
        stdout=subprocess.PIPE,
    )
    p.wait()
    id_, err = p.communicate()

    return id_.strip()
