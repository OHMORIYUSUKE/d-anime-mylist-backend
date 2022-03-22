from sqlalchemy import create_engine

from models.mylist import Base
from models.db.db import DATABASE

engine = create_engine(DATABASE, echo=True)


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Create Table! ✨ 🍰 ✨")


if __name__ == "__main__":
    main()
