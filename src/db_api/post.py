from sqlalchemy import func
from schema.posts import Posts
from . import tag
from . import user

def get(session, data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 1}
    try:
        if data.get('post_id') and data.get('site') and data.get('title'):
            post = session.query(Posts).filter(Posts.post_id == data['post_id'])\
                .filter(Posts.site == data['site'])\
                .filter(Posts.title == data['title']).one()
        elif data.get('site') and data.get('title'):
            post = session.query(Posts).filter(Posts.site == data['site'])\
                .filter(Posts.title == data['title']).one()
        elif data.get('post_id'):
            post = session.query(Posts).filter(Posts.post_id == data['post_id']).one()
        else:
            errors.append('Post not found')
            post = None
    except Exception as e:
        errors.append(e)
        post = None
    return {'errors': errors, 'result': post}

def create(session, data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 1}

    try:            
        # TAGS
        tags_obj = []
        if len(data['tags']) >=1:
            for tag_name in data['tags']:
                tag_data = {'site': data['site'], 'name': tag_name}
                tag_result = tag.get(session=session, data=tag_data)
                if not tag_result.get('errors'):
                    tag_obj = tag_result['result']
                    tags_obj.append(tag_obj)
            
        # OWNER USER
        owner_obj = None
        if data.get('owner_user_id'):
            owner_data = {'site': data['site'], 'user_id': data['owner_user_id']}
            owner_result = user.get(session=session, data=owner_data)
            if not owner_result.get('errors'):
                owner_obj = owner_result['result']
            else:
                errors.extend(owner_result['errors'])
        
        # EDITOR USER
        editor_obj = None
        if data.get('last_editor_user_id'):
            editor_data = {'site': data['site'], 'user_id': data['last_editor_user_id']}
            editor_result = user.get(session=session, data=editor_data)
            if not editor_result.get('errors'):
                editor_obj = editor_result['result']
            else:
                errors.extend(editor_result['errors'])

        # Check if question exist
        question_exists = False
        question_obj = None
        if data.get('post_type_id', 0) == 2 and data.get('parent_id'):
            question_data = {'site': data['site'], 'post_id': data['parent_id']}
            question_result = get(session=session, data=question_data)
            if not question_result.get('errors'):
                question_exists = True
                question_obj = question_result['result']
            else:
                errors.extend(question_result['errors'])

        post = Posts(
            post_id=data['post_id'],
            title=data.get('title'),
            clean_title=data.get('clean_title'),
            post_type=data['post_type'],
            score=data.get('score', 0),
            view_count=data.get('view_count', 0),
            parent_id=question_obj.id if question_obj else None,
            body=data.get('body'),
            owner_user_id=owner_obj.id if owner_obj else None,
            last_editor_user_id=editor_obj.id if editor_obj else None,
            tags=tags_obj,
            answer_count=data.get('answer_count', 0),
            comment_count=data.get('comment_count', 0),
            last_edited_date=data.get('last_edited_date'),
            last_activity_date=data.get('last_activity_date'),
            created_time=data.get('created_time'),
            site=data['site'],
        )
        result = 1
        session.add(post)
        session.commit()
    except Exception as e:
        errors.append(e)
        result = 0

    return {'errors': errors, 'result': result}