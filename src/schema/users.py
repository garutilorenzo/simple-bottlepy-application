# coding=utf-8

from sqlalchemy import func, text, Column, String, Integer, Date, Boolean, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from .base import Base
from .posts import Posts
from .network import Sites


class Users(Base):
    __tablename__ = 'users'
    
    __table_args__ = (UniqueConstraint('network_sites', 'user_id', 'name', name='uk_users_site_id_name'),)

    id = Column(Integer, primary_key=True)
    site = Column(ENUM(Sites), name="network_sites")
    user_id = Column(Integer)
    
    name = Column(String(100), index=True)
    clean_name = Column(String(80))

    reputation = Column(Integer)
    website = Column(String(200))
    location = Column(String(80))
    about_me = Column(Text)
    views = Column(Integer)
    up_votes = Column(Integer)
    down_votes = Column(Integer)
    account_id = Column(Integer)

    posts = relationship(
        "Posts",
        foreign_keys=[Posts.owner_id],
        back_populates="owner",
    )
    edited_posts = relationship(
        "Posts",
        foreign_keys=[Posts.editor_id],
        back_populates="editor",
    )

    last_access_time = Column(DateTime(timezone=True))
    created_time = Column(DateTime(timezone=True))
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    def as_dict(self):
       return {c.name: str(getattr(self, 'site' if c.name == 'network_sites' else c.name)) for c in self.__table__.columns if c.name}