from xml.etree.ElementTree import iterparse

import json,csv,re,os,time
from multiprocessing import Process

from sqlalchemy.sql.expression import insert
import xml.etree.ElementTree as ET

import utils
import db_api

from schema.network import Sites
from schema.posts import PostType

DATA_DIRECTORY = '/data/'
MAX_BULK_ITEMS = 4000

def clenaup_string(s, max_lenght=80):
    translate_string = s.\
    translate(str.maketrans({"'":None})).\
    translate(str.maketrans({"&":'and'})).\
    translate(str.maketrans({".":None}))
    clean_string = re.sub('[^A-Za-z0-9]+', '-', translate_string)
    clean_string = clean_string.replace('--','-')
    
    result = clean_string
    if clean_string.endswith('-'):
        result = ''.join(clean_string.rsplit('-', 1))
    return result.lower()[:max_lenght]

def count_rows(filename):
    num_lines = sum(1 for line in open(filename) if '<row' in line)
    return num_lines

def console_log(site, entity, count, start, items_count):
    time_reset = False
    if count % 200 == 0:
        time_diff = time.time() - start
        print('Site name-entity: {}-{}'.format(site.name, entity))
        print('Parsed 200 items in: {}'.format(time_diff))
        print('Remaining items: {}'.format(items_count - count))
        print('-'*90)
        time_reset = True
    return time_reset

def my_xml_to_dict(filename):
    for _, elem in iterparse(filename, events=("end",)):
        if elem.tag == "row":
            new_dict = {}
            for k in elem.attrib.keys():
                new_dict['@{}'.format(k)] = elem.attrib[k]

            elem.clear()
            yield new_dict

def parse_tags(session, site, dirname):
    filename = '{}/Tags.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
    tags_start = time.time()
    tags_counter = 0
    tags_count = count_rows(filename)

    for r in res:
        search_data = {'tag_id': r['@Id'], 'site': site, 'name': r['@TagName']}
        tag_result = db_api.tag.get(session=session, filters=search_data)
        if not tag_result.get('result'):
            clean_name = clenaup_string(s=r['@TagName'])
            insert_data = {
                'site': site,
                'tag_id': r['@Id'],
                'name': r['@TagName'],
                'clean_name': clean_name,
                'questions': r['@Count'],
            }
            tag_insert = db_api.tag.create(session=session, data=insert_data)
            
            # LOG
            tags_counter +=1
            time_reset = console_log(site, 'tags', tags_counter, tags_start, tags_count)
            if time_reset:
                tags_start = time.time()
            # END-LOG

def parse_users(session, site, dirname):
    bulk_insert_count = 0
    objects_list = []
    
    filename = '{}/Users.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
    users_start = time.time()
    users_counter = 0
    users_count = count_rows(filename)

    for r in res:
        search_data = {'user_id': r['@Id'], 'site': site, 'name': r['@DisplayName']}
        user_result = db_api.user.get(session=session, filters=search_data)
        if not user_result.get('result'):
            clean_name = clenaup_string(s=r['@DisplayName'])
            insert_data = {
                'site': site,
                'user_id': r['@Id'],
                'name': r['@DisplayName'],
                'clean_name': clean_name,
                'reputation': int(r['@Reputation']),
                'website': r.get('@WebsiteUrl', ''),
                'location': r.get('@Location', ''),
                'about_me': r.get('@AboutMe', ''),
                'views': int(r.get('@Views', '')),
                'up_votes': int(r.get('@UpVotes', 0)),
                'down_votes': int(r.get('@DownVotes', 0)),
                'account_id': int(r.get('@AccountId', 0)),
                'created_time': r.get('@CreationDate'),
                'last_access_time': r.get('@LastAccessDate'),
            }
            user_insert = db_api.user.create(session=session, data=insert_data, commit=False)
            if not user_insert.get('error'):
                bulk_insert_count +=1
                objects_list.append(user_insert['user'])
            else:
                print(user_insert['error'])
                print(site.name)
            
            # LOG
            users_counter +=1
            time_reset = console_log(site, 'users', users_counter, users_start, users_count)
            if time_reset:
                users_start = time.time()
            # END-LOG

            if bulk_insert_count == MAX_BULK_ITEMS:
                bulk_save_result = db_api.utils.bulk_save(session=session, obj_list=objects_list)
                print('Commit user errors: {errors}'.format(**bulk_save_result))
                print('Commit user result: {result}'.format(**bulk_save_result))
                bulk_insert_count = 0
                objects_list = []
    
    # Object not committed
    bulk_save_result = db_api.utils.bulk_save(session=session, obj_list=objects_list)
    #

def parse_posts(session, site, dirname):
    bulk_insert_count = 0
    objects_list = []

    filename = '{}/Posts.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
    posts_start = time.time()
    posts_counter = 0
    posts_count = count_rows(filename)

    for r in res:
              
        search_data = {'post_id': r['@Id'], 'site': site, 'title': r.get('@Title', '')}
        post_result = db_api.post.get(session=session, filters=search_data)
        
        if not post_result.get('result'):
            post_type = utils.get_post_type(int(r['@PostTypeId']))
            clean_title = clenaup_string(s=r.get('@Title', ''))
            
            if not post_type:
                continue
                
            insert_data = {
                'site': site,
                'post_id': int(r['@Id']),
                'title': r.get('@Title', ''),
                'clean_title': clean_title,
                'post_type_id': int(r['@PostTypeId']),
                'post_type': post_type,
                'score': int(r['@Score']),
                'view_count': int(r.get('@ViewCount', 0)),
                'parent_id': int(r.get('@ParentId', 0)),
                'accepted_answer_id': int(r.get('@AcceptedAnswerId', 0)),
                'body': r.get('@Body', ''),
                'owner_user_id': int(r.get('@OwnerUserId', 0)),
                'last_editor_user_id': int(r.get('@LastEditorUserId', 0)),
                'raw_tags': r.get('@Tags', ''),
                'answer_count': int(r.get('@AnswerCount', 0)),
                'comment_count': int(r.get('@CommentCount', 0)),
                'last_edited_date': r.get('@LastEditDate'),
                'last_activity_date': r.get('@LastActivityDate'),
                'created_time': r.get('@CreationDate'),
            }
            
            insert_data['tags'] = ''
            if insert_data.get('raw_tags'):
                tags_split = insert_data['raw_tags'].split('>')
                clean_tags = [t.replace('<','') for t in tags_split if t != '']
                insert_data['tags'] = clean_tags
            post_insert = db_api.post.create(session=session, data=insert_data, add=True, commit=False)

            if not post_insert.get('error'):
                bulk_insert_count +=1
            
            # LOG
            posts_counter +=1
            time_reset = console_log(site, 'posts', posts_counter, posts_start, posts_count)
            if time_reset:
                posts_start = time.time()
            # END-LOG

            if bulk_insert_count == MAX_BULK_ITEMS:
                bulk_save_result = db_api.utils.commit(session=session)
                print('Commit post errors: {errors}'.format(**bulk_save_result))
                print('Commit post result: {result}'.format(**bulk_save_result))
                bulk_insert_count = 0

    bulk_save_result = db_api.utils.commit(session=session)

def parse_post_history(session, site, dirname):
    bulk_insert_count = 0
    objects_list = []

    filename = '{}/PostHistory.xml'.format(dirname)
    res = my_xml_to_dict(filename)

    post_h_start = time.time()
    post_h_counter = 0
    post_h_count = count_rows(filename)

    for r in res:
        
        search_data = {'post_history_id': r['@Id'], 'site': site, 'post_id': int(r['@PostId'])}

        post_history_result = db_api.post_history.get(session=session, filters=search_data)
        if not post_history_result.get('result'):
            
            post_history_type = utils.get_post_history_type(int(r['@PostHistoryTypeId']))

            insert_data = {
                'site': site,
                'post_history_id': int(r['@Id']),
                'post_id': int(r['@PostId']),
                'post_history_type': post_history_type,
                'revision_guid': r['@RevisionGUID'],
                'user_id': int(r.get('@UserId', 0)),
                'body': r.get('@Text', ''),
                'comment': r.get('@Comment', ''),
                'created_time': r.get('@CreationDate'),
            }
            
            post_history_insert = db_api.post_history.create(session=session, data=insert_data, commit=False)
            if not post_history_insert.get('error'):
                bulk_insert_count +=1
                objects_list.append(post_history_insert['post_history'])
            
             # LOG
            post_h_counter +=1
            time_reset = console_log(site, 'post_history', post_h_counter, post_h_start, post_h_count)
            if time_reset:
                post_h_start = time.time()
            # END-LOG

            if bulk_insert_count == MAX_BULK_ITEMS:
                bulk_save_result = db_api.utils.bulk_save(session=session, obj_list=objects_list)
                print('Commit post_history errors: {errors}'.format(**bulk_save_result))
                print('Commit post_history result: {result}'.format(**bulk_save_result))
                bulk_insert_count = 0
                objects_list = []
    
    # Object not committed
    bulk_save_result = db_api.utils.bulk_save(session=session, obj_list=objects_list)
    #


def import_multiprocess(dirs):
    
    with db_api.utils.db_session() as session:
        jobs = []
        for dirname in dirs:
            site_name = dirname.replace(DATA_DIRECTORY,'')
            site = getattr(Sites, site_name)
            p = Process(target=parse_tags, args=(session,site,dirname))
            jobs.append(p)
            p.start()
            
        for job in jobs:
            job.join()
    
    print('Finish import tags')

    with db_api.utils.db_session() as session:
        jobs = []
        for dirname in dirs:
            site_name = dirname.replace(DATA_DIRECTORY,'')
            site = getattr(Sites, site_name)
            p = Process(target=parse_users, args=(session,site,dirname))
            jobs.append(p)
            p.start()
            
        for job in jobs:
            job.join()
    
    print('Finish import users')

    with db_api.utils.db_session() as session:
        jobs = []
        for dirname in dirs:
            site_name = dirname.replace(DATA_DIRECTORY,'')
            site = getattr(Sites, site_name)
            p = Process(target=parse_posts, args=(session,site,dirname))
            jobs.append(p)
            p.start()
            
        for job in jobs:
            job.join()
    
    print('Finish import posts')

    with db_api.utils.db_session() as session:
        jobs = []
        for dirname in dirs:
            site_name = dirname.replace(DATA_DIRECTORY,'')
            site = getattr(Sites, site_name)
            p = Process(target=parse_post_history, args=(session,site,dirname))
            jobs.append(p)
            p.start()
            
        for job in jobs:
            job.join()
    
    print('Finish import post_history')

if __name__ == '__main__':
    dirs = [x[0] for x in os.walk(DATA_DIRECTORY) if x[0] != DATA_DIRECTORY]
    import_multiprocess(dirs)