from sqlalchemy import func
from schema.tags import Tags

def get(session, filters):
    errors = []
    if not filters:
        errors.append('no filter provided')
        return {'errors': errors, 'result': 0}
    try:
        tag = session.query(Tags).filter_by(**filters).one()
    except Exception as e:
        errors.append(e)
        tag = None
    return {'errors': errors, 'result': tag}

def get_all(session, offset=1, limit=50):
    errors = []
    try:
        tags = session.query(Tags)
        if limit:
            tags = tags.limit(limit)

        if offset:
            offset -= 1
            tags = tags.offset(offset*limit)
    except Exception as e:
        errors.append(e)
        tags = None
    return {'errors': errors, 'result': tags}

def count(session):        
    return session.query(func.count(Tags.id)).scalar() 

def create(session, data, commit=True):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    try:
        tag = Tags(
            tag_id=data['tag_id'],
            name=data['name'],
            clean_name=data['clean_name'],
            questions=data['questions'],
            site=data['site'],
        )
        result = 1
        if commit:
            session.add(tag)
            session.commit()
    except Exception as e:
        errors.append(e)
        result = 0
        tag = None

    return {'errors': errors, 'result': result, 'tag': tag}
