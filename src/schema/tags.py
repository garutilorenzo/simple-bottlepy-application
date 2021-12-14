# coding=utf-8

from sqlalchemy import func, text, Column, String, Integer, Date, Boolean, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM

from .base import Base
from .network import Sites


class Tags(Base):
    __tablename__ = 'tags'

    __table_args__ = (UniqueConstraint('network_sites', 'tag_id', 'name', name='uk_tags_site_id_name'),)

    id = Column(Integer, primary_key=True)
    site = Column(ENUM(Sites), name="network_sites")
    tag_id = Column(Integer)
    name = Column(String(100), index=True)
    clean_name = Column(String(80))
    questions = Column(Integer)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())

    def as_dict(self):
       return {c.name: str(getattr(self, 'site' if c.name == 'network_sites' else c.name)) for c in self.__table__.columns if c.name}