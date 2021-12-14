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

def get_all_filtered(session, offset=None, limit=None, filters={}):
    errors = []

    query_filters = {}
    del_keys = ['network_name']

    for k in filters.keys():
        if filters[k] and k not in del_keys:
            query_filters[k] = filters[k]

        if k == 'network_name':
            site_result = network.get(network_name=filters['network_name'])
            if not site_result.get('errors'):
                query_filters['site'] = site_result['result']
    try:
        tags = session.query(Tags).filter_by(**query_filters)
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

def get_json(session, offset=None, limit=None, filters={}):
    result = {'errors': [], 'data': [], 'last_page': 0, 'items': 0}
    
    if filters:
        tags_result = get_all_filtered(session=session, offset=offset, limit=limit, filters=filters)
    else:
        tags_result = get_all(session=session, offset=offset, limit=limit)

    if not tags_result.get('errors'):
        result['items'] =  tags_result['count']
        result['last_page'] =  int(tags_result['count']/limit)
        for tag in tags_result['result']:
            result['data'].append(tag.as_dict())
    else:
        result['errors'].extend(tags_result['errors'])
        return result
    return result

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
