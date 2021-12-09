from contextlib import contextmanager
from schema.base import Session

@contextmanager
def db_session():
    session = Session()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()