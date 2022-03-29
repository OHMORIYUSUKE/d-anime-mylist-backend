from fastapi.testclient import TestClient
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))

from main import app
from db import DATABASE
from models.mylist import Base

engine = create_engine(DATABASE, echo=True)

client = TestClient(app)


# 正常なID
id = "O10cMRZUU1Dj72JH"
# DBに存在しないID
invalid_id_db = "zpkoYm76a9lYzeED"
# ページが存在存在しないID
invalid_id_page = "invalid_id"
# 不正なURL
invalid_url = "https://anime.dmkt-sp.jp/animestore/"

DANIME_MYLISTPAGE_BASE_URL = "https://anime.dmkt-sp.jp/animestore/public_list"


def main():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Create Table! ✨ 🍰 ✨")


if __name__ == "__main__":
    main()
