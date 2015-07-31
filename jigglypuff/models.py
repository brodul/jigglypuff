from sqlalchemy import (
    Table,
    Column,
    Index,
    Integer,
    ForeignKey,
    Text,
    Unicode,
)

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
)

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

board_song = Table(
    'boards_songs', Base.metadata,
    Column('board_id', Integer, ForeignKey('boards.id')),
    Column('song_id', Integer, ForeignKey('songs.id')),
    Index('idx_board_song', 'board_id', 'song_id'),
    Index('idx_song_board', 'song_id', 'board_id'),
)


class Board(Base):
    __tablename__ = 'boards'
    id = Column(Integer, primary_key=True)

    name = Column(Unicode, unique=False)
    # owner = Column(Unicode, unique=False)

    songs = relationship(
        "Song",
        secondary=board_song,
        backref="boards"
    )

    def get_dict(self):
        """@todo: Docstring for get_dict

        :returns: @todo

        """

        songs = dict((song.file_id, song.get_dict()) for song in self.songs)
        return {
            'name': self.name,
            'songs': songs,
        }


class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    youtube_id = Column(Text, unique=True)

    title = Column(Unicode, unique=False)
    length = Column(Unicode, unique=False)

    file_id = Column(Text, unique=True)

    status = Column(Unicode, unique=False)

    def get_dict(self):
        """@todo: Docstring for get_dict

        :returns: @todo

        """

        return {
            'file_id': self.file_id,
            'title': self.title,
            'length': self.length,
            'youtube_id': self.youtube_id,
        }
