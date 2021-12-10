import os, sys, json

from bottle_sa import SQLAlchemyPlugin
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

# Template default variables
SimpleTemplate.defaults["url"] = lambda: request.url
SimpleTemplate.defaults["fullpath"] = lambda: request.fullpath
SimpleTemplate.defaults["nav_pages"] = utils.build_nav_pages()
SimpleTemplate.defaults["nav_dropdown_pages"] = utils.build_nav_dropdown_pages()

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
    return dict(page_name='home')

@app.route('/docs')
@view('docs')
def index(db):
    return dict(page_name='docs')

@app.route('/users')
@app.route('/users/<page_nr:int>')
@view('users')
def get_users(db, page_nr=1):
    current_url = request.url
    current_page = current_url.split('/')[3]

    users = []
    users_result = db_api.user.get_all(offset=page_nr, session=db)
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
    current_url = request.url
    current_page = current_url.split('/')[3]

    user_result = db_api.user.get(session=db, filters={'id': id})
    if not user_result.get('error'):
        user = user_result['result']
    return dict(page_name=current_page , user=user)


@app.route('/tags')
@app.route('/tags/<page_nr:int>')
@view('tags')
def get_tags(db, page_nr=1):
    current_url = request.url
    current_page = current_url.split('/')[3]

    tags = []
    tags_result = db_api.tag.get_all(offset=page_nr, session=db)
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

@app.route('/posts')
@app.route('/posts/<page_nr:int>')
@view('posts')
def get_posts(db, page_nr=1):
    current_url = request.url
    current_page = current_url.split('/')[3]

    posts = []
    count_all_posts = 0
    posts_result = db_api.post.get_all_filtered(offset=page_nr, session=db, only_questions=True)
    if not posts_result.get('errors'):
        posts = posts_result['result']
        count_all_posts = posts_result['count']
    
    res = dict(
        page_name=current_page, 
        posts=posts, 
        records=count_all_posts, 
        page_nr=page_nr,
    )
    return res

@app.route('/post/<id:int>/<post_title>')
@view('post')
def get_post(db, id=0, post_title=''):
    current_url = request.url
    current_page = current_url.split('/')[3]

    posts_result = db_api.post.get(session=db, filters={'id': id})
    if not posts_result.get('error'):
        post = posts_result['result']
    return dict(page_name=current_page , post=post)


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=main_config.get('http_port', 8080), reloader=main_config['enable_reloader'], debug=main_config['enable_debug'])
    # run(app, host='0.0.0.0')