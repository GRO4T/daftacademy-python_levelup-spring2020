# app/database/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

SQLALCHEMY_DATABASE_URL = os.environ['DATABASE_URL']

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
