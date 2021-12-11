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
        session.rollback()
        errors.append(e)
        result = 0

    return {'errors': errors, 'result': result}

def bulk_add(session, obj_list):
    errors = []
    if not obj_list:
        errors.append('missing object list')
        return {'errors': errors, 'result': 0}
    
    try:
        session.add_all(obj_list)
        session.commit()
        result = 1
    except Exception as e:
        session.rollback()
        errors.append(e)
        result = 0

    return {'errors': errors, 'result': result}


def commit(session):
    errors = []
    try:
        session.commit()
        result = 1
    except Exception as e:
        session.rollback()
        errors.append(e)
        result = 0

    return {'errors': errors, 'result': result}