import db_api

# # DB-Schema
from schema.base import Session, engine, Base
from schema.tags import Tags
from schema.users import Users
from schema.posts import Posts, PostHistory
from schema.network import Sites


if __name__ == '__main__':
    with db_api.utils.db_session() as session:
        # user_result = db_api.user.get(session=session, data={'user_id': 4})
        # user = user_result['result']
        # for post in user.posts:
        #     print(post.title)
        #     print(post.id)
    
        # post_result = db_api.post.get(session=session, data={'post_id': 522})
        # post = post_result['result']
        # print(post.question)

        # user = session.query(Users).filter(Users.id == 10)

        # tags_result = db_api.tag.count(session=session)
        # print(tags_result)
        filters = {'post_id': True}
        posts = session.query(Posts).filter_by(**filters)
        print(posts)