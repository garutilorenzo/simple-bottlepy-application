from redis_schema import PostsTags

def get(filters):
    errors = []
    if not filters:
        errors.append('no filter provided')
        return {'errors': errors, 'result': 0}
    try:
        if filters.get('tag_name') and filters.get('post_id'):
            post_tag = PostsTags.query.filter(tag_name=filters['tag_name'])\
                .filter(post_id=filters['post_id'])\
                .filter(site=filters['site']).all()
        elif filters.get('tag_name') and filters.get('site'):
            post_tag = PostsTags.query.filter(tag_name=filters['tag_name'])\
                    .filter(site=filters['site']).all()
        elif filters.get('tag_name'):
            post_tag = PostsTags.query.filter(tag_name=filters['tag_name']).all()
    except Exception as e:
        errors.append(e)
        post_tag = None
    return {'errors': errors, 'result': post_tag}

def get_all():
    pass

def create(data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    for k,v in data.items():
        if isinstance(data[k], str):
            data[k] = v.encode('utf-8')
            
    try:
        post_tag = PostsTags(
            site=data['site'],
            tag_id=data['tag_id'],
            tag_name=data['tag_name'],
            post_id=data['post_id'],
        )
        post_tag.save()
        result = 1
    except Exception as e:
        errors.append(e)
        result = 0
        post_tag = None

    return {'errors': errors, 'result': result, 'tag': post_tag}