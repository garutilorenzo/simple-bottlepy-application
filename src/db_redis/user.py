from redis_schema import Users

def get(filters):
    errors = []
    if not filters:
        errors.append('no filter provided')
        return {'errors': errors, 'result': 0}
    try:
        if filters.get('id'):
            user = Users.query.filter(id=filters['id']).all()
        elif filters.get('user_id'):
            user = Users.query.filter(user_id=filters['user_id'])\
                .filter(site=filters['site']).all()
    except Exception as e:
        errors.append(e)
        user = None
    return {'errors': errors, 'result': user}

def get_all(offset=None, limit=None):
    errors = []
    try:
        offset -= 1
        users = Users.query.limit(offset, limit).execute()
        count = Users.query.count()
    except Exception as e:
        count = 0
        errors.append(e)
        users = None
    return {'errors': errors, 'result': users, 'count': count}

def create(data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    for k,v in data.items():
        if isinstance(data[k], str):
            data[k] = v.encode('utf-8')
    try:
        user = Users(
            user_id=data['user_id'],
            name=data['name'],
            clean_name=data['clean_name'],
            reputation=data['reputation'],
            website=data.get('website', ''),
            location=data.get('location', '')[:80],
            about_me=data.get('about_me', ''),
            views=data.get('views', 0),
            up_votes=data.get('up_votes', 0),
            account_id=data.get('account_id', 0),
            down_votes=data.get('down_votes', 0),
            last_access_time=data.get('last_access_time'),
            created_time=data.get('created_time'),
            site=data['site'],
        )
        user.save()
        result = 1
    except Exception as e:
        errors.append(e)
        result = 0
        user = None

    return {'errors': errors, 'result': result, 'user': user}