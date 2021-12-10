import time
import socket
import bottle

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession


class SQLAlchemyPlugin(object):

    name = 'sqlalchemy'
    api = 2

    def __init__(self, engine, metadata=None, keyword='db', create=False, create_session=None, config={}):
        
        self.engine = engine
        if create_session is None:
            create_session = sessionmaker()
        self.create_session = create_session
        self.metadata = metadata
        self.keyword = keyword
        self.create = create
        self.config = config

    def setup(self, app):
        ''' Make sure that other installed plugins don't affect the same
            keyword argument and check if metadata is available.'''
        for other in app.plugins:
            if not isinstance(other, SQLAlchemyPlugin):
                continue
            if other.keyword == self.keyword:
                raise bottle.PluginError("Found another SQLAlchemy plugin with "\
                                  "conflicting settings (non-unique keyword).")
            elif other.name == self.name:
                self.name += '_%s' % self.keyword
        if self.create and not self.metadata:
            raise bottle.PluginError('Define metadata value to create database.')
    
    def apply(self, callback, route):
        if self.create:
            self.wait()
            self.metadata.create_all(self.engine)

        def wrapper(*args, **kwargs):
            kwargs[self.keyword] = session = self.create_session(bind=self.engine)
            try:
                rv = callback(*args, **kwargs)
            except (SQLAlchemyError, bottle.HTTPError):
                session.rollback()
                raise
            except bottle.HTTPResponse:
                raise
            finally:
                if isinstance(self.create_session, ScopedSession):
                    self.session.remove()
                else:
                    session.close()
            return rv

        return wrapper
    
    def wait(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.connect((self.config['pgsql_host'], self.config['pgsql_port']))
                s.close()
                break
            except socket.error as ex:
                time.sleep(1)