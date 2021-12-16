from redis_schema import Posts

from . import tag
from . import user
from . import post_tag
from db_api import network

def slicing(obcet_list, offset=0, limit=0):
    return obcet_list[offset:(offset + limit)]

def get(filters):
    errors = []
    if not filters:
        errors.append('no filter provided')
        return {'errors': errors, 'result': 0}
    try:
        if filters.get('id'):
            post = Posts.query.filter(id=filters['id']).all()
        elif filters.get('post_id'):
            post = Posts.query.filter(post_id=filters['post_id'])\
                .filter(site=filters['site']).all()
    except Exception as e:
        errors.append(e)
        post = None
    return {'errors': errors, 'result': post}


def get_all(offset=None, limit=None):
    errors = []
    try:
        offset -= 1
        posts = Posts.query.limit(offset, limit).execute()
        count = Posts.query.count()
    except Exception as e:
        count = 0
        errors.append(e)
        posts = None
    return {'errors': errors, 'result': posts, 'count': count}

def get_all_filtered(offset=None, limit=None, filters={}, filters_like={}):
    errors = []
    
    query_filters = {}   
    filters_like_keys = [k for k in filters_like.keys()]
    del_keys = ['only_questions', 'network_name'] + filters_like_keys

    for k in filters.keys():
        if filters[k] and k not in del_keys:
            query_filters[k] = filters[k]
            
        if k == 'network_name':
            site_result = network.get(network_name=filters['network_name'])
            if not site_result.get('errors'):
                query_filters['site'] = site_result['result']
    
    try:
        posts = []
        question_ids = []
        if query_filters.get('tag'):
            filters_data = {'tag_name': query_filters['tag']}
            if query_filters.get('site'):
                filters_data['site'] = query_filters['site'].name    
            post_tag_result = post_tag.get(filters=filters_data)
            if post_tag_result.get('errors'):
                 errors.extend(tag_result['errors'])
            else:
                for r_post_tag in  post_tag_result['result']:
                    question_ids.append(r_post_tag.post_id)
        
            
            for q_id in question_ids:
                posts_ = Posts.query\
                    .filter(post_id=q_id)\
                    .filter(post_type='question')
                if filters_like.get('title'):
                    posts_ = posts_.filter(title=filters_like['title'])
                
                posts_ = posts_.all()
                posts.extend(posts_)
                
                offset -= 1
                posts = slicing(posts, offset, limit)
                count = len(posts)
        else:
            posts = Posts.query\
                .filter(post_type='question')
            if query_filters.get('site'):
                posts = posts.filter(site=query_filters['site'].name)\
                    
            if filters_like.get('title'):
                posts = posts.filter(title=filters_like['title'])
            count = posts.count()
            
            offset -= 1
            posts = posts.limit(offset, limit).execute()
            
    except Exception as e:
        errors.append(e)
        posts = None
        count = 0
    return {'errors': errors, 'result': posts, 'count': count}

def create(data):
    errors = []
    if not data:
        errors.append('missing input data')
        return {'errors': errors, 'result': 0}

    for k,v in data.items():
        if isinstance(data[k], str):
            data[k] = v.encode('utf-8')
    
    # TAGS
    tags_obj = []
    if len(data['tags']) >=1:
        for tag_name in data['tags']:
            filters_data = {'site': data['site'], 'name': tag_name}
            tag_result = tag.get(filters=filters_data)
            if tag_result.get('errors'):
                 errors.extend(tag_result['errors'])
            else:
                if len(tag_result.get('result')) > 0:
                    for r_tag in tag_result['result']:
                        post_tag_insert_data = {
                            'site': data['site'],
                            'tag_id': r_tag.tag_id,
                            'tag_name': r_tag.name,
                            'post_id': data['post_id']
                        }
                        tag_insert = post_tag.create(data=post_tag_insert_data)
                        if tag_insert.get('errors'):
                            errors.extend(tag_result['errors'])
        
    # OWNER USER
    owner_obj = None
    if data.get('owner_user_id'):
        filters_owner = {'site': data['site'], 'user_id': data['owner_user_id']}
        owner_result = user.get(filters=filters_owner)
        if owner_result.get('errors'):
            errors.extend(owner_result['errors'])
        elif len(owner_result['result']) == 0:
            errors.append('No user found')
        else:
            owner_obj = owner_result['result'][0]
            
    
    # EDITOR USER
    editor_obj = None
    if data.get('last_editor_user_id'):
        filters_owner = {'site': data['site'], 'user_id': data['last_editor_user_id']}
        editor_result = user.get(filters=filters_owner)
        if editor_result.get('errors'):
            errors.extend(editor_result['errors'])
        elif len(editor_result['result']) == 0:
            errors.append('No user found')
        else:
            editor_obj = editor_result['result'][0]

    # Check if question exist
    question_exists = False
    question_obj = None
    if data['post_type_id'] == 2 and data.get('parent_id'):
        filter_question = {'site': data['site'], 'post_id': data['parent_id']}
        question_result = get(filters=filter_question)
        if question_result.get('errors'):
            errors.extend(question_result['errors'])
        elif len(question_result['result']) == 0:
            errors.append('No question found')
        else:
            question_exists = True
            question_obj = question_result['result'][0]      

    try:
        post = Posts(
            post_id=data['post_id'],
            title=data.get('title'),
            clean_title=data.get('clean_title'),
            post_type=data['post_type'],
            score=data.get('score', 0),
            view_count=data.get('view_count', 0),
            parent_id=data['parent_id'],
            body=data.get('body'),
            question=question_obj if question_obj else None,
            owner=owner_obj if owner_obj else None,
            editor=editor_obj if editor_obj else None,
            answer_count=data.get('answer_count', 0),
            comment_count=data.get('comment_count', 0),
            last_edited_date=data.get('last_edited_date'),
            last_activity_date=data.get('last_activity_date'),
            created_time=data.get('created_time'),
            site=data['site'],
        )
        
        post.save()
        result = 1
    except Exception as e:
        errors.append(e)
        result = 0
        post = None

    return {'errors': errors, 'result': result, 'post': post}
