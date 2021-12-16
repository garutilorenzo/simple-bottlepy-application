from xml.etree.ElementTree import iterparse

import json,csv,re,os,datetime
from multiprocessing import Process

import xmltodict
import xml.etree.ElementTree as ET

import utils
import db_redis
from schema.network import Sites

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

def my_xml_to_dict(filename):
    for _, elem in iterparse(filename, events=("end",)):
        if elem.tag == "row":
            new_dict = {}
            for k in elem.attrib.keys():
                new_dict['@{}'.format(k)] = elem.attrib[k]

            elem.clear()
            yield new_dict

def parse_tags(site, dirname):
    filename = '{}/Tags.xml'.format(dirname)
    res = my_xml_to_dict(filename)
        
    for r in res:
        search_data = {'tag_id': r['@Id'], 'site': site.name}
        tag_result = db_redis.tag.get(filters=search_data)
        if len(tag_result.get('result')) == 0:
            clean_name = clenaup_string(s=r['@TagName'])
            insert_data = {
                'site': site.name,
                'tag_id': r['@Id'],
                'name': r['@TagName'],
                'clean_name': clean_name,
                'questions': r['@Count'],
                'created_time': datetime.datetime.now(),
            }
            tag_insert = db_redis.tag.create(data=insert_data)
            print(tag_insert)

def parse_users(site, dirname):    
    filename = '{}/Users.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
    for r in res:
        search_data = {'user_id': r['@Id'], 'site': site.name}
        user_result = db_redis.user.get(filters=search_data)
        if len(user_result.get('result')) == 0:
            clean_name = clenaup_string(s=r['@DisplayName'])
            created_time = datetime.datetime.fromisoformat(r.get('@CreationDate'))
            last_access_time = datetime.datetime.fromisoformat(r.get('@LastAccessDate'))
            insert_data = {
                'site': site.name,
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
                'last_access_time': last_access_time,
                'created_time': created_time,
            }
            user_insert = db_redis.user.create(data=insert_data)
            print(user_insert)

def parse_posts(site, dirname):
    filename = '{}/Posts.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
    for r in res:
              
        search_data = {'post_id': r['@Id'], 'site': site.name}
        post_result = db_redis.post.get(filters=search_data)
        if len(post_result.get('result')) == 0:
            post_type = utils.get_post_type(int(r['@PostTypeId']))
            clean_title = clenaup_string(s=r.get('@Title', ''))
            
            if not post_type:
                continue
            
            created_time = datetime.datetime.fromisoformat(r.get('@CreationDate'))
            last_activity_date = datetime.datetime.fromisoformat('1900-01-01 00:00:00')
            if r.get('@LastActivityDate'):
                last_activity_date = datetime.datetime.fromisoformat(r.get('@LastActivityDate'))
            
            last_edited_date = datetime.datetime.fromisoformat('1900-01-01 00:00:00')
            if r.get('@LastEditDate'):
                last_edited_date = datetime.datetime.fromisoformat(r.get('@LastEditDate'))

            insert_data = {
                'site': site.name,
                'post_id': int(r['@Id']),
                'title': r.get('@Title', ''),
                'clean_title': clean_title,
                'post_type_id': int(r['@PostTypeId']),
                'post_type': post_type.name,
                'score': int(r['@Score']),
                'view_count': int(r.get('@ViewCount', 0)),
                'parent_id': int(r.get('@ParentId', 0)),
                'body': r.get('@Body', ''),
                'owner_user_id': int(r.get('@OwnerUserId', 0)),
                'last_editor_user_id': int(r.get('@LastEditorUserId', 0)),
                'raw_tags': r.get('@Tags', ''),
                'answer_count': int(r.get('@AnswerCount', 0)),
                'comment_count': int(r.get('@CommentCount', 0)),
                'last_edited_date': last_edited_date,
                'last_activity_date': last_activity_date,
                'created_time': created_time,
            }
            
            insert_data['tags'] = ''
            if insert_data.get('raw_tags'):
                tags_split = insert_data['raw_tags'].split('>')
                clean_tags = [t.replace('<','') for t in tags_split if t != '']
                insert_data['tags'] = clean_tags
            post_insert = db_redis.post.create(data=insert_data)
            print(post_insert)

def parse_post_history(site, dirname):
    filename = '{}/PostHistory.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
    for r in res:
        
        search_data = {'post_history_id': r['@Id'], 'site': site.name, 'post_id': int(r['@PostId'])}

        post_history_result = db_redis.post_history.get(filters=search_data)
        if len(post_history_result.get('result')) == 0:
            
            created_time = datetime.datetime.fromisoformat(r.get('@CreationDate'))
            post_history_type = utils.get_post_history_type(int(r['@PostHistoryTypeId']))

            if not post_history_type:
                continue

            insert_data = {
                'site': site.name,
                'post_history_id': int(r['@Id']),
                'post_id': int(r['@PostId']),
                'post_history_type': post_history_type.name,
                'revision_guid': r['@RevisionGUID'],
                'user_id': int(r.get('@UserId', 0)),
                'body': r.get('@Text', ''),
                'comment': r.get('@Comment', ''),
                'created_time': created_time,
            }
            
            post_history_insert = db_redis.post_history.create(data=insert_data)
            print(post_history_insert)

def import_multiprocess(dirs):
    jobs = []
    for dirname in dirs:
        site_name = dirname.replace(DATA_DIRECTORY,'')
        site = getattr(Sites, site_name)
        p = Process(target=parse_tags, args=(site,dirname))
        jobs.append(p)
        p.start()
        
    for job in jobs:
        job.join()
    
    print('Finish import tags')

    jobs = []
    for dirname in dirs:
        site_name = dirname.replace(DATA_DIRECTORY,'')
        site = getattr(Sites, site_name)
        p = Process(target=parse_users, args=(site,dirname))
        jobs.append(p)
        p.start()
        
    for job in jobs:
        job.join()
    
    print('Finish import users')

    jobs = []
    for dirname in dirs:
        site_name = dirname.replace(DATA_DIRECTORY,'')
        site = getattr(Sites, site_name)
        p = Process(target=parse_posts, args=(site,dirname))
        jobs.append(p)
        p.start()
        
    for job in jobs:
        job.join()
    
    print('Finish import posts')

    jobs = []
    for dirname in dirs:
        site_name = dirname.replace(DATA_DIRECTORY,'')
        site = getattr(Sites, site_name)
        p = Process(target=parse_post_history, args=(site,dirname))
        jobs.append(p)
        p.start()
        
    for job in jobs:
        job.join()
    
    print('Finish import post_history')

if __name__ == '__main__':
    dirs = [x[0] for x in os.walk(DATA_DIRECTORY) if x[0] != DATA_DIRECTORY]
    import_multiprocess(dirs)