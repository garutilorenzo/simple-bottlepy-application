from sqlalchemy import func
from schema.posts import Posts, PostType
from . import tag
from . import user

def get(session, filters):
    errors = []
    if not filters:
        errors.append('no filter provided')
        return {'errors': errors, 'result': 0}
    try:
        post = session.query(Posts).filter_by(**filters).one()
    except Exception as e:
        errors.append(e)
        post = None
    return {'errors': errors, 'result': post}

def get_all(session, offset=1, limit=50):
    errors = []
    try:
        posts = session.query(Posts)
        if limit:
            posts = posts.limit(limit)

        if offset:
            offset -= 1
            posts = posts.offset(offset*limit)
    except Exception as e:
        errors.append(e)
        posts = None
    return {'errors': errors, 'result': posts}

def get_all_filtered(session, offset=1, limit=50, filters={}, only_questions=False):
    errors = []
    
    if only_questions:
        filters['parent_id'] = None
        filters['post_type'] = PostType.question
    
    try:
        posts = session.query(Posts).filter_by(**filters)
        count = posts.count()

        if limit:
            posts = posts.limit(limit)

        if offset:
            offset -= 1
            posts = posts.offset(offset*limit)
    except Exception as e:
        errors.append(e)
        posts = None
        count = 0
    return {'errors': errors, 'result': posts, 'count': count}

def count(session):        
    return session.query(func.count(Posts.id)).scalar() 

def create(session, data, add=True, commit=True):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    try:            
        # TAGS
        tags_obj = []
        if len(data['tags']) >=1:
            for tag_name in data['tags']:
                filters_data = {'site': data['site'], 'name': tag_name}
                tag_result = tag.get(session=session, filters=filters_data)
                if not tag_result.get('errors'):
                    tag_obj = tag_result['result']
                    tags_obj.append(tag_obj)
            
        # OWNER USER
        owner_obj = None
        if data.get('owner_user_id'):
            filters_owner = {'site': data['site'], 'user_id': data['owner_user_id']}
            owner_result = user.get(session=session, filters=filters_owner)
            if not owner_result.get('errors'):
                owner_obj = owner_result['result']
            else:
                errors.extend(owner_result['errors'])
        
        # EDITOR USER
        editor_obj = None
        if data.get('last_editor_user_id'):
            filters_editor = {'site': data['site'], 'user_id': data['last_editor_user_id']}
            editor_result = user.get(session=session, filters=filters_editor)
            if not editor_result.get('errors'):
                editor_obj = editor_result['result']
            else:
                errors.extend(editor_result['errors'])

        # Check if question exist
        question_exists = False
        question_obj = None
        if data.get('post_type_id', 0) == 2 and data.get('parent_id'):
            filter_question = {'site': data['site'], 'post_id': data['parent_id']}
            question_result = get(session=session, filters=filter_question)
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
        
        if add:
            session.add(post)
        if commit:
            session.commit()
    except Exception as e:
        errors.append(e)
        result = 0
        post = None

    return {'errors': errors, 'result': result, 'post': post}