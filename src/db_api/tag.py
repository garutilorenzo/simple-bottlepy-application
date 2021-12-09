from sqlalchemy import func
from schema.tags import Tags

def get(session, data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 1}
    try:
        if data.get('tag_id') and data.get('site') and data.get('name'):
            tag = session.query(Tags).filter(Tags.tag_id == data['tag_id'])\
                .filter(Tags.site == data['site'])\
                .filter(Tags.name == data['name']).one()
        elif data.get('site') and data.get('name'):
            tag = session.query(Tags).filter(Tags.site == data['site'])\
                .filter(Tags.name == data['name']).one()
        elif data.get('id'):
            tag = session.query(Tags).filter(Tags.id == data['id']).one()
        elif data.get('tag_id'):
            tag = session.query(Tags).filter(Tags.tag_id == data['tag_id']).one()
        elif data.get('name'):
            tag = session.query(Tags).filter(Tags.name == data['name']).one()
        else:
            errors.append('Tag not found')
            tag = None
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

def create(session, data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 1}

    try:
        tag = Tags(
            tag_id=data['tag_id'],
            name=data['name'],
            clean_name=data['clean_name'],
            questions=data['questions'],
            site=data['site'],
        )
        result = 1
        session.add(tag)
        session.commit()
    except Exception as e:
        errors.append(e)
        result = 0
    return {'errors': errors, 'result': result}
