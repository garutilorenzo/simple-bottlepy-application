from schema.posts import PostType, PostHistoryType
from schema.network import Sites

def get_post_type(post_type_id):
    for post_type in PostType:
        if int(post_type.value) == post_type_id:
            return post_type
    return None

def get_post_history_type(post_history_id):
    for post_history_type in PostHistoryType:
        if int(post_history_type.value) == post_history_id:
            return post_history_type
    return None