from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from db import Base, ENGINE


class Mylists(Base):
    __tablename__ = "mylist"
    id = Column("id", String(255), primary_key=True, nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(), nullable=False)
    updated_at = Column("updated_at", DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class MylistContents(Base):
    __tablename__ = "mylistContents"
    id = Column("id", String(255), primary_key=True, nullable=False)
    title = Column("title", String(255), primary_key=True)
    image = Column("image", String(255))
    url = Column("url", String(255))
    first = Column("first", String(255))
    stories = Column("stories", String(255))
