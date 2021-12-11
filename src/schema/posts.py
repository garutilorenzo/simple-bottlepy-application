# coding=utf-8
import enum

from sqlalchemy import func, text, Table, ForeignKey, Column, String, Text, Integer, Date, Boolean, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, backref

from .base import Base
from .tags import Tags
from .network import Sites

post_tag_association = Table(
    'post_tag', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class PostType(enum.Enum):
    question = 1
    answer = 2

class PostHistoryType(enum.Enum):
    initial_title = 1
    initial_body = 2
    initial_tags = 3
    edit_title = 4
    edit_body = 5
    edit_tags = 6
    rollback_title = 7
    rollback_body = 8
    rollback_tags = 9
    post_closed = 10
    post_reopened = 11
    post_deleted = 12
    post_undeleted = 13
    post_locked = 14
    post_unlocked = 15
    community_owned = 16
    post_migrated = 17
    question_merged = 18
    question_protected = 19
    question_unprotected = 20
    post_disassociated = 21
    question_unmerged = 22

class CloseReason(enum.Enum):
    exact_duplicate = 1
    off_topic = 2
    subjective = 3
    not_a_real_question = 4
    too_localized = 7

class Posts(Base):
    __tablename__ = 'posts'
    
    __table_args__ = (UniqueConstraint('network_sites', 'post_id', 'title', name='uk_posts_site_id_title'),)

    id = Column(Integer, primary_key=True)
    site = Column(ENUM(Sites), name="network_sites")
    
    title = Column(String(400))
    clean_title = Column(String(80))
    
    post_id = Column(Integer)

    parent_id = Column(Integer, ForeignKey('posts.id'))
    question = relationship("Posts", remote_side=[id], backref='answers')
    
    post_type = Column(ENUM(PostType), name="post_type")
    
    score = Column(Integer, default=0)
    view_count = Column(Integer, default=0)
    body = Column(Text)
    
    owner_user_id = Column(Integer, ForeignKey('users.id'))
    owner_user = relationship("Users", foreign_keys=[owner_user_id], back_populates="posts")

    last_editor_user_id = Column(Integer, ForeignKey('users.id'))
    last_editor_user = relationship("Users", foreign_keys=[last_editor_user_id], back_populates="edited_posts")
    
    tags = relationship("Tags", secondary=post_tag_association)

    post_history = relationship("PostHistory", back_populates="post")

    answer_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    last_edited_date = Column(DateTime(timezone=True))
    last_activity_date = Column(DateTime(timezone=True))
    created_time = Column(DateTime(timezone=True))
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

class PostHistory(Base):
    __tablename__ = 'post_history'

    __table_args__ = (UniqueConstraint('network_sites', 'post_history_id', name='uk_site_post_history_id'),)

    id = Column(Integer, primary_key=True)
    site = Column(ENUM(Sites), name="network_sites")
    post_history_id = Column(Integer) 

    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Posts", foreign_keys=[post_id], back_populates="post_history")

    post_history_type = Column(ENUM(PostHistoryType), name="post_history_type")
    revision_guid = Column(String(40))
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("Users", foreign_keys=[user_id])

    text = Column(Text)
    comment = Column(String(500))

    created_time = Column(DateTime(timezone=True))
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())
