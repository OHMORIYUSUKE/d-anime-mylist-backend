from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os

# 接続したいDBの基本情報を設定
DB_USER_NAME = os.environ.get("DB_USER_NAME")
DB_PW = os.environ.get("DB_PW")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

DATABASE = "mysql://%s:%s@%s/%s?charset=utf8" % (
    DB_USER_NAME,
    DB_PW,
    DB_HOST,
    DB_NAME,
)

# DBとの接続
ENGINE = create_engine(DATABASE, encoding="utf-8", echo=True)

# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するか
    sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
)

# modelで使用する
Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
# DB接続用のセッションクラス、インスタンスが作成されると接続する
Base.query = session.query_property()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
