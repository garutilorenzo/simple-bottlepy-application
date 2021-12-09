# coding=utf-8
import load_config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

main_config = load_config.load_config()
conn_string = 'postgresql+psycopg2://{pgsql_username}:{pgsql_password}@{pgsql_host}:{pgsql_port}/{pgsql_db}'.format(**main_config)

engine = create_engine(conn_string, pool_size=80, pool_recycle=60)
Session = sessionmaker(bind=engine)

Base = declarative_base()