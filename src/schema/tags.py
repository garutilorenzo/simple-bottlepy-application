# coding=utf-8

from sqlalchemy import func, text, Column, String, Integer, Date, Boolean, DateTime
from sqlalchemy.dialects.postgresql import ENUM

from .base import Base
from .network import Sites


class Tags(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    site = Column(ENUM(Sites), name="network_sites")
    tag_id = Column(Integer)
    name = Column(String(100), index=True, unique=True)
    clean_name = Column(String(80))
    questions = Column(Integer)
    created_time = Column(DateTime(timezone=True), server_default=func.now())
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())