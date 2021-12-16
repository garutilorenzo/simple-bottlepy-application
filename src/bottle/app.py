import os, sys, json, urllib

from bottle_sa import SQLAlchemyPlugin
from bottle_cache import RedisCache
from schema.base import engine
from schema.base import Base

from bottle import Bottle, run, \
     template, view, debug, static_file, request, response, redirect, TEMPLATE_PATH, SimpleTemplate
import utils, load_config, db_api

main_config = load_config.load_config()

dirname = '/app/src/{}/'.format(os.getenv('BOTTLE_APP_NAME'))

TEMPLATE_PATH.insert(0, '{}/views/'.format(dirname))

# Main Bottle app/application
app = application = Bottle()

# DB Plugin
saPlugin = SQLAlchemyPlugin(
    engine=engine, metadata=Base.metadata, 
    create=main_config['create_db_schema'], 
    config=main_config,
)
application.install(saPlugin)

# Cache
cache = RedisCache()

# Template default variables
SimpleTemplate.defaults["url"] = lambda: request.url
SimpleTemplate.defaults["fullpath"] = lambda: request.fullpath
SimpleTemplate.defaults["nav_pages"] = utils.build_nav_pages()
SimpleTemplate.defaults["nav_dropdown_pages"] = utils.build_nav_dropdown_pages()
SimpleTemplate.defaults["default_result_limit"] = main_config['default_result_limit']

debug(main_config['enable_debug'])

@app.route('/static/<filename:re:.*\.css>')
def send_css(filename, db):
    response = static_file(filename, root=dirname+'/static/asset/css')
    response.set_header("Cache-Control", "public, max-age=604800")
    return response

@app.route('/static/<filename:re:.*\.js>')
def send_js(filename, db):
    response = static_file(filename, root=dirname+'/static/asset/js')
    response.set_header("Cache-Control", "public, max-age=604800")
    return response

@app.route('/static/<filename:re:.*\.map>')
def send_js(filename, db):
    response = static_file(filename, root=dirname+'/static/asset/map_files')
    response.set_header("Cache-Control", "public, max-age=604800")
    return response

@app.route('/static/img/<filename:path>')
def send_img(filename, db):
    response = static_file(filename, root=dirname+'/static/asset/img')
    response.set_header("Cache-Control", "public, max-age=604800") 
    return response

@app.route('/sitemap.xml')
def send_sitemap_xml(db):
    response = static_file('sitemap.xml', root=dirname+'/static/sitemaps/')
    response.content_type = 'application/xml'
    return response

@app.route('/robots.txt')
def send_robots(db):
    response = static_file('robots.txt', root=dirname+'/static/robots/')
    response.content_type = 'text/plain'
    return response

@app.route('/<filename:re:.*\.gz>')
def send_sitemap_gz(filename, db):
    response = static_file(filename, root=dirname+'/static/sitemaps/')
    response.content_type = 'application/gzip'
    return response

@app.error(404)
@view('index')
def error404(db):
    return dict(page_name='404', error_message='Nothing here, sorry')

@app.route('/')
@view('index')
def index(db):
    network_sites_result = db_api.network.get_all()
    if not network_sites_result.get('error'):
        network_sites = network_sites_result['result']
    return dict(page_name='home', network_sites=network_sites)

@app.route('/docs')
@view('docs')
def index(db):
    return dict(page_name='docs')

@app.route('/users')
@app.route('/users/<page_nr:int>')
@view('users')
def get_users(db, page_nr=1):
    current_page = utils.get_first_level_url(request)

    users = []
    users_result = db_api.user.get_all(limit=main_config['default_result_limit'], offset=page_nr, session=db)
    if not users_result.get('errors'):
        users = users_result['result']

    count_all_users = db_api.user.count(session=db)
    
    res = dict(
        page_name=current_page, 
        users=users, 
        records=count_all_users, 
        page_nr=page_nr,
    )
    return res

@app.route('/user/<id:int>/<user_name>')
@view('user')
def get_user(db, id=0, user_name=''):
    current_page = utils.get_first_level_url(request)

    user_result = db_api.user.get(session=db, filters={'id': id})
    if not user_result.get('error'):
        user = user_result['result']
    return dict(page_name=current_page , user=user)


@app.route('/tags')
@app.route('/tags/<page_nr:int>')
@cache.cached()
@view('tags')
def get_tags(db, page_nr=1):
    current_page = utils.get_first_level_url(request)

    tags = []
    tags_result = db_api.tag.get_all(limit=main_config['default_result_limit'], offset=page_nr, session=db)
    if not tags_result.get('errors'):
        tags = tags_result['result']

    count_all_tags = db_api.tag.count(session=db)
    
    res = dict(
        page_name=current_page, 
        tags=tags, 
        records=count_all_tags, 
        page_nr=page_nr,
    )
    return res

@app.route('/posts', method='POST')
@cache.cached()
@view('posts')
def post_search_posts(db, page_nr=1):
    
    forms = request.POST.getall('searchQuestionForm')
    network = request.forms.get('network_site')
    question_tag = request.forms.get('question_tag')
    question_title = request.forms.get('question_title')
    
    filters = {
        'network_name': network if network else '',
        'tag': question_tag.split(':::')[1] if question_tag else '',
        'only_questions': True,
    }

    filters_like = {
        'title': question_title if question_title else '',
    }

    current_page = utils.get_first_level_url(request)

    posts = []
    count_all_posts = 0
    posts_result = db_api.post.get_all_filtered(
        limit=main_config['default_result_limit'], 
        offset=page_nr, session=db, 
        filters=filters,
        filters_like=filters_like,
    )

    if not posts_result.get('errors'):
        posts = posts_result['result']
        count_all_posts = posts_result['count']
    
    dict_parameters = {**filters, **filters_like}

    res = dict(
        page_name=current_page, 
        posts=posts, 
        records=count_all_posts, 
        page_nr=page_nr,
        parameters=urllib.parse.urlencode(dict_parameters),
    )
    return res

@app.route('/posts')
@app.route('/posts/<page_nr:int>')
@cache.cached()
@view('posts')
def get_posts(db, page_nr=1):
    
    raw_parameters = dict(request.query.decode())
    filters = {
        'network_name': raw_parameters.get('network_name', ''),
        'tag': raw_parameters.get('tag', ''),
        'only_questions':  raw_parameters.get('only_questions', ''),
    }

    filters_like = {
        'title': raw_parameters.get('title', ''),
    }

    current_page = utils.get_first_level_url(request)

    posts = []
    count_all_posts = 0
    posts_result = db_api.post.get_all_filtered(
        limit=main_config['default_result_limit'], 
        offset=page_nr, session=db, 
        filters=filters,
        filters_like=filters_like,
    )

    if not posts_result.get('errors'):
        posts = posts_result['result']
        count_all_posts = posts_result['count']

    dict_parameters = {**filters, **filters_like}
    
    res = dict(
        page_name=current_page, 
        posts=posts, 
        records=count_all_posts, 
        page_nr=page_nr,
        parameters=urllib.parse.urlencode(dict_parameters),
    )
    return res

@app.route('/post/<id:int>/<post_title>')
@view('post')
def get_post(db, id=0, post_title=''):
    current_page = utils.get_first_level_url(request)

    posts_result = db_api.post.get(session=db, filters={'id': id})
    if not posts_result.get('error'):
        post = posts_result['result']
    return dict(page_name=current_page , post=post)

### API - UTILS ###

@app.route('/api/autocomplete/form/get_tags', method='POST')
def api_get_tags(db):
    result = {'errors': [], 'data': [], 'count': 0}

    network_site = request.forms.get("network_site")
    auth_key = request.forms.get("auth_key")
    
    if not auth_key or auth_key != 'f883af4981c6d.bcdb777cebe0ab5aa76,277ddca765f616c03a9c5629afcb5798!e1513':
        response.status = 401
        response.set_header("Content-Type", 'application/json')
        error = {'error': 'access denied'}
        return json.dumps(error, indent=4, sort_keys=True)

    tags_result = db_api.tag.get_all_filtered(session=db, filters={'network_name': network_site})
    if not tags_result.get('errors'):
        result['count'] = tags_result['count']
        for t in tags_result['result']:
            t_dict = {
                'value': '{}:::{}'.format(str(t.id), t.name),
                'text': t.name
            }
            result['data'].append(t_dict)

    else:
        result['errors'].extend(tags_result['errors'])
        

    # return 200 Success
    response.set_header("Content-Type", 'application/json')
    return json.dumps(result, indent=4, sort_keys=True)

### END API - UTILS ###

### API-REST ###

@app.route('/api/get/tags', method='POST')
@cache.cached(content_type='application/json')
def api_get_tags(db):
    result = {'errors': [], 'data': []}
    params = ['tag_name', 'network_name', 'auth_key']
   
    # parse input data
    try:
        data = request.json
    except ValueError:
        response.status = 400
        response.set_header("Content-Type", 'application/json')
        result['errors'].append('Value error, only application/json objects acepted')
        return json.dumps(result, indent=4, sort_keys=True)
    
    
    for key in data.keys():
        if key not in params:
            response.status = 400
            response.set_header("Content-Type", 'application/json')
            result['errors'].append('{} params not acepted'.format(key))
            return json.dumps(result, indent=4, sort_keys=True)
    
    for value in params:
        data[value] = data.get(value, '')
    
    data['page'] = int(data.get('page', 1))
    data['limit'] = int(data.get('limit', 200))
    if data['limit'] > 200:
        data['limit'] = 200
    if not data['auth_key'] or data['auth_key'] != 'dd4d5ff1c13!28356236c402d7ada.aed8b797ebd299b942291bc66,f804492be2009f14':
        response.status = 401
        response.set_header("Content-Type", 'application/json')
        result['errors'].append('access denied')
        return json.dumps(result, indent=4, sort_keys=True)

    filters = {
        'network_name': data['network_name'],
        'name': data['tag_name'],
    }
    tags_result = db_api.tag.get_json(session=db, offset=data['page'], limit=data['limit'])
    if not tags_result.get('errors'):
        result['data'].extend(tags_result['data'])
        result['items'] = tags_result['items']
        result['last_page'] = tags_result['last_page']
    else:
        result['errors'].extend(tags_result['errors'])

    # return 200 Success
    response.set_header("Content-Type", 'application/json')
    return json.dumps(result, indent=4, sort_keys=True)

### END API-REST ###

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=main_config.get('http_port', 8080), reloader=main_config['enable_reloader'], debug=main_config['enable_debug'])
    # run(app, host='0.0.0.0')