from sqlalchemy import func
from schema.posts import PostHistory
from . import post
from . import user

def get(session, filters):
    errors = []
    if not filters:
        errors.append('no filter provided')
        return {'errors': errors, 'result': 0}
    try:
        post_history = session.query(PostHistory).filter_by(**filters).one()
    except Exception as e:
        errors.append(e)
        post_history = None
    return {'errors': errors, 'result': post_history}

def create(session, data, commit=True):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}
    try:
        # POST
        question_exists = False
        question_obj = None
        if data.get('post_id'):
            filter_post = {'site': data['site'], 'post_id': data['post_id']}
            question_result = post.get(session=session, filters=filter_post)
            if not question_result.get('errors'):
                question_exists = True
                question_obj = question_result['result']
            else:
                errors.extend(question_result['errors'])
        
        # OWNER USER
        user_obj = None
        if data.get('user_id'):
            filter_owner = {'site': data['site'], 'user_id': data['user_id']}
            user_result = user.get(session=session, filters=filter_owner)
            if not user_result.get('errors'):
                user_obj = user_result['result']
            else:
                errors.extend(user_result['errors'])

        post_history = PostHistory(
            post_history_id= data['post_history_id'],
            post_id=question_obj.id if question_obj else None,
            post_history_type=data['post_history_type'],
            revision_guid=data.get('revision_guid', ''),
            user_id=user_obj.id if user_obj else None,
            text=data.get('body', ''),
            comment=data.get('comment', ''),
            created_time=data.get('created_time'),
            site=data['site'],
        )
        result = 1
        if commit:
            session.add(post_history)
            session.commit()
    except Exception as e:
        result = 0
        errors.append(e)
        post_history = None

    return {'errors': errors, 'result': result, 'post_history': post_history}