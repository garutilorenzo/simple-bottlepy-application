# coding=utf-8

from sqlalchemy.dialects import postgresql

from schema.base import Session, engine, Base
from schema.tags import Tags
from schema.users import Users
from schema.posts import Posts
from schema.network import Sites

Base.metadata.create_all(engine)