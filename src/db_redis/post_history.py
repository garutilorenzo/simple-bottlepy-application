from redis_schema import PostHistory

from . import user
from . import post

def get(filters):
    errors = []
    if not filters:
        errors.append('no filter provided')
        return {'errors': errors, 'result': 0}
    try:
        if filters.get('post_history_id'):
            post_history = PostHistory.query.filter(post_history_id=filters['post_history_id'])\
                    .filter(post_id=filters['post_id'])\
                    .filter(site=filters['site']).all()
    except Exception as e:
        errors.append(e)
        post_history = None
    return {'errors': errors, 'result': post_history}

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
        # POST
        question_exists = False
        question_obj = None
        if data.get('post_id'):
            filter_post = {'site': data['site'], 'post_id': data['post_id']}
            question_result = post.get(filters=filter_post)
            if question_result.get('errors'):
                errors.extend(question_result['errors'])
            elif len(question_result['result']) == 0:
                errors.append('No question found')
            else:
                question_exists = True
                question_obj = question_result['result'][0]
                
        # OWNER USER
        user_obj = None
        if data.get('user_id'):
            filters_owner = {'site': data['site'], 'user_id': data['user_id']}
            owner_result = user.get(filters=filters_owner)
            if owner_result.get('errors'):
                errors.extend(owner_result['errors'])
            elif len(owner_result['result']) == 0:
                errors.append('No user found')
            else:
                user_obj = owner_result['result'][0]

        post_history = PostHistory(
            post_history_id= data['post_history_id'],
            post_id= data['post_id'],
            post=question_obj if question_obj else None,
            post_history_type=data['post_history_type'],
            revision_guid=data.get('revision_guid', ''),
            user=user_obj if user_obj else None,
            text=data.get('body', ''),
            comment=data.get('comment', ''),
            created_time=data.get('created_time'),
            site=data['site'],
        )
        post_history.save()
        result = 1
    except Exception as e:
        result = 0
        errors.append(e)
        post_history = None

    return {'errors': errors, 'result': result, 'post_history': post_history}