from sqlalchemy import func
from schema.tags import Tags
from . import network

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

def get_all(session, offset=None, limit=None):
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

def get_all_filtered(session, offset=None, limit=None, filters={}):
    errors = []

    if filters.get('network_name'):
        site_result = network.get(network_name=filters['network_name'])
        if not site_result.get('errors'):
            filters['site'] = site_result['result']
        del filters['network_name']
    
    try:
        tags = session.query(Tags).filter_by(**filters)
        count = tags.count()
        if limit:
            tags = tags.limit(limit)

        if offset:
            offset -= 1
            tags = tags.offset(offset*limit)
    except Exception as e:
        errors.append(e)
        tags = None
        count = 0

    return {'errors': errors, 'result': tags, 'count': count}

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
        session.rollback()
        errors.append(e)
        result = 0
        tag = None

    return {'errors': errors, 'result': result, 'tag': tag}
