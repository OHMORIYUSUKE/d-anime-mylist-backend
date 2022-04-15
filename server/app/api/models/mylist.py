from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from db import Base, ENGINE


class Mylist(Base):
    __tablename__ = "mylist"
    mylist_id = Column("mylist_id", String(255), primary_key=True, nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(), nullable=False)
    updated_at = Column("updated_at", DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)


class MylistContents(Base):
    __tablename__ = "mylistContents"
    mylist_id = Column("mylist_id", String(255), primary_key=True, nullable=False)
    anime_id = Column("anime_id", String(255), primary_key=True, nullable=False)


class AnimeInfo(Base):
    __tablename__ = "animeInfo"
    anime_id = Column("anime_id", String(255), primary_key=True, nullable=False)
    title = Column("title", String(255), primary_key=True, nullable=False)
    image = Column("image", String(255), nullable=False)
    url = Column("url", String(255), nullable=False)
    first = Column("first", String(255), nullable=False) # 1話タイトル
    stories = Column("stories", String(255), nullable=False) # 話数
