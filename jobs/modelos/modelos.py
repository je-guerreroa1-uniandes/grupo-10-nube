from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    filename = Column(String(250))
    to_extension = Column(String(128))
    processed_filename = Column(String(250))
    state = Column(String(20))
    user_id = Column(Integer)
    created_at = Column(String(128))
    updated_at = Column(String(128))