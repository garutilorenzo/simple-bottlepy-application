from schema.posts import PostType, PostHistoryType
from schema.network import Sites

META_COSTRAINT = {
    'base': 'A very simple BottlePy application with SqlAlchemy support',
    'base_page': 'A very simple BottlePy application with SqlAlchemy support - {}',
}

class Meta(object):
    def __init__(self, title, description):
        self.title = title
        self.description = description

class StaticPage(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url

def build_meta(page_name=None, title=None):
    if title:
        title = title[:80]
        description = title[:150]
    elif page_name:
        title = description = META_COSTRAINT['base_page'].format(page_name)
    else:
        title = description = META_COSTRAINT['base']
    meta = Meta(title=title, description=description)
    return meta

def build_nav_pages():
    pages = []
    
    pages_list = [
        ('Home', '/'),
        ('Tags', '/tags'),
        ('Posts', '/posts'),
        ('Users', '/users'),
    ]
    
    for page in pages_list:
        item = StaticPage(name=page[0], url=page[1])
        pages.append(item)
    
    return pages

def build_nav_dropdown_pages():
    pages = []
    
    pages_list = [
        ('Docs', '/docs'),
    ]
    
    for page in pages_list:
        item = StaticPage(name=page[0], url=page[1])
        pages.append(item)
    
    return pages

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

def get_first_level_url(request):
    current_url = request.url
    first_level_url = current_url.\
        split('/')[3].\
        split('?', 1)[0]
    return first_level_url