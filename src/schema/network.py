# coding=utf-8
import enum
from sqlalchemy import func, text, Column, String, Integer, Date, Boolean, DateTime
from .base import Base

class Sites(enum.Enum):
    vi = 'vi.stackexchange.com'
    workplace = 'workplace.stackexchange.com'
    wordpress = 'wordpress.stackexchange.com'
    unix = 'unix.stackexchange.com'
    tex = 'tex.stackexchange.com'