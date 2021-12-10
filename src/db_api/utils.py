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

def bulk_save(session, obj_list):
    errors = []
    if not obj_list:
        errors.append('missing object list')
        return {'errors': errors, 'result': 0}
    
    try:
        session.bulk_save_objects(obj_list)
        session.commit()
        result = 1
    except Exception as e:
        result = 0

    return {'errors': errors, 'result': result}