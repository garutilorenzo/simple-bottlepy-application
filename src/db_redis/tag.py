from redis_schema import Tags

def get(filters):
    errors = []
    if not filters:
        errors.append('no filter provided')
        return {'errors': errors, 'result': 0}
    try:
        if filters.get('tag_id'):
            tag = Tags.query.filter(tag_id=filters['tag_id'])\
                    .filter(site=filters['site']).all()
        elif filters.get('name'):
            tag = Tags.query.filter(name=filters['name'])\
                    .filter(site=filters['site']).all()
    except Exception as e:
        errors.append(e)
        tag = None
    return {'errors': errors, 'result': tag}

def get_all(offset, limit):
    errors = []
    try:
        offset -= 1
        tags = Tags.query.limit(offset, limit).execute()
        count = Tags.query.count()
    except Exception as e:
        errors.append(e)
        tags = None
        count = 0
    return {'errors': errors, 'result': tags, 'count': count}

def create(data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    for k,v in data.items():
        if isinstance(data[k], str):
            data[k] = v.encode('utf-8')
            
    try:
        tag = Tags(
            tag_id=data['tag_id'],
            name=data['name'],
            clean_name=data['clean_name'],
            questions=data['questions'],
            site=data['site'],
            created_time=data['created_time']
        )
        tag.save()
        result = 1
    except Exception as e:
        errors.append(e)
        result = 0
        tag = None

    return {'errors': errors, 'result': result, 'tag': tag}