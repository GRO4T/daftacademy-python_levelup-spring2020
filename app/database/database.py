# app/database/database.py

import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import yaml

connection: sqlite3.Connection

SQLALCHEMY_DATABASE_URL = '';

# load postgres url from an yaml file
postgres_conf = {}
try:
    with open('app/database/postgres_url_local.yml') as yaml_file:
        postgres_conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
except FileNotFoundError:
    with open('app/database/postgres_url.yml') as yaml_file:
        postgres_conf = yaml.load(yaml_file.read(), Loader=yaml.SafeLoader)
SQLALCHEMY_DATABASE_URL = postgres_conf.get("postgres").get("url")
print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
