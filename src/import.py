from xml.etree.ElementTree import iterparse

import json,csv,re,os

from sqlalchemy.sql.expression import insert
import xmltodict
import xml.etree.ElementTree as ET

import utils
import db_api

from schema.network import Sites
from schema.posts import PostType

DATA_DIRECTORY = '/data/'
MAX_BULK_ITEMS = 8000

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

# def xml_to_dict(filename):
#     xml_tree = ET.parse(filename)

#     root = xml_tree.getroot()
#     to_string  = ET.tostring(root, encoding='UTF-8', method='xml')

#     return xmltodict.parse(to_string)

def parse_tags(session, site, dirname):
    filename = '{}/Tags.xml'.format(dirname)
    res = my_xml_to_dict(filename)
        
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
            print(tag_insert['result'])

def parse_users(session, site, dirname):
    bulk_insert_count = 0
    objects_list = []
    
    filename = '{}/Users.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
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
            
            if bulk_insert_count == MAX_BULK_ITEMS:
                bulk_save_result = db_api.utils.bulk_save(session=session, obj_list=objects_list)
                print('Commit user errors: {errors}'.format(**bulk_save_result))
                print('Commit user result: {result}'.format(**bulk_save_result))
                bulk_insert_count = 0
                objects_list = []
    
    # Object not committed
    session.bulk_save_objects(objects_list)
    session.commit()
    #

def parse_posts(session, site, dirname):
    bulk_insert_count = 0
    objects_list = []

    filename = '{}/Posts.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
    for r in res['posts']['row']:
              
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
            post_insert = db_api.post.create(session=session, data=insert_data)
            print(post_insert['result'])
    
def parse_post_history(session, site, dirname):
    bulk_insert_count = 0
    objects_list = []

    filename = '{}/PostHistory.xml'.format(dirname)
    res = my_xml_to_dict(filename)
    
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
            
            if bulk_insert_count == MAX_BULK_ITEMS:
                bulk_save_result = db_api.utils.bulk_save(session=session, obj_list=objects_list)
                print('Commit post_history errors: {errors}'.format(**bulk_save_result))
                print('Commit post_history result: {result}'.format(**bulk_save_result))
                bulk_insert_count = 0
                objects_list = []
    
    # Object not committed
    session.bulk_save_objects(objects_list)
    session.commit()
    #

if __name__ == '__main__':
    # site = Sites.vi
    # print(site)
    # with db_api.utils.db_session() as session:
    #     # parse_tags(session, site)
    #     # parse_users(session, site)
    #     parse_posts(session, site)
    #     parse_post_history(session, site)
    dirs = [x[0] for x in os.walk(DATA_DIRECTORY) if x[0] != DATA_DIRECTORY]
    for dirname in dirs:
        with db_api.utils.db_session() as session:
            site_name = dirname.replace(DATA_DIRECTORY,'')
            site = getattr(Sites, site_name)
            
            parse_tags(session, site, dirname)
            parse_users(session, site, dirname)
            parse_posts(session, site, dirname)
            parse_post_history(session, site, dirname)