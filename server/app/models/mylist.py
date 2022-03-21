from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from models.db.db import Base, ENGINE

class Mylists(Base):
    __tablename__ = 'mylist'
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    created_at = Column('created_at', TIMESTAMP, server_default=current_timestamp())

class MylistContents(Base):
    __tablename__ = 'mylistContents'
    id = Column(String(255),primary_key=True)
    title = Column(String(255),primary_key=True)
    image = Column(String(255))
    url = Column(String(255))


def main():
    Base.metadata.drop_all(bind=ENGINE)
    Base.metadata.create_all(bind=ENGINE)


if __name__ == "__main__":
    main()