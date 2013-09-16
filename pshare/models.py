import os
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from . import utils
from .settings import settings

DATABASE_FILENAME = settings.database_filename
DATABASE_URL = 'sqlite:///%s' % (DATABASE_FILENAME)

engine = create_engine(DATABASE_URL, echo = settings.debug)

Session = sessionmaker(bind = engine)
session = Session()

Base = declarative_base()

class Pad(Base):
    __tablename__ = 'pads'

    id = Column(Integer, primary_key = True)
    owner_id = Column(String(128))
    pad_id = Column(String(128))

    messages = relationship('Message', backref = 'pad', cascade = 'all, delete, delete-orphan')

    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.pad_id = utils.random.transform(owner_id, length = settings.public_id_length)

    @property
    def oid(self):
        return self.owner_id

    @property
    def pid(self):
        return self.pad_id

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key = True)
    pad_id = Column(Integer, ForeignKey('pads.pad_id'))
    content = Column(Text)

    def __init__(self, pad_id, content):
        self.pad_id = pad_id
        self.content = content

def open():
    if not os.path.exists(DATABASE_FILENAME):
        Base.metadata.create_all(engine)

def close():
    session.close()
