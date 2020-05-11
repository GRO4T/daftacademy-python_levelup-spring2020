import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

connection: sqlite3.Connection

SQLALCHEMY_DATABASE_URL = "postgresql://chinook:chinook@postgresserver/chinook"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost:5432/chinook"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


