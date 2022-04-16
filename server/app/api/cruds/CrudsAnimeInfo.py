from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime

import models.mylist as mylist_model
import schemas.mylist as mylist_schema


class CrudsAnimeInfo:
    def __init__(self) -> None:
        pass

    """
    animenfoテーブル
    """

    def get_by_animeId(self, db: Session, anime_id: str) -> List[mylist_model.AnimeInfo]:
        return db.query(mylist_model.AnimeInfo).filter(mylist_model.AnimeInfo.anime_id == anime_id).first()

    def create(self, db: Session, anime_info: mylist_model.AnimeInfo) -> mylist_model.AnimeInfo:
        db_anime_info = mylist_model.AnimeInfo(anime_info)
        db.add(db_anime_info)
        db.commit()
        db.refresh(db_anime_info)
        return db_anime_info

    def update(db: Session, anime_info: mylist_model.AnimeInfo) -> mylist_model.AnimeInfo:
        db_anime_info = db.query(mylist_model.AnimeInfo).filter(mylist_model.AnimeInfo.anime_id == anime_info.anime_id)
        db_anime_info.update({mylist_model.AnimeInfo.stories: anime_info.stories})
        db.commit()
        return db_anime_info
