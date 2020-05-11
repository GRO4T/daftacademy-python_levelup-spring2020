from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

Base = declarative_base()
class OrmArtist(Base):
    __tablename__ = 'artist'

    artist_id = Column(Integer, primary_key=True)
    name = Column(String(120))
