from sqlalchemy.orm import Session
from sqlalchemy import exc
from typing import List
from datetime import datetime
from typing import TypeVar, Union
import models.mylist as mylist_model
import schemas.mylist as mylist_schema

from fastapi import FastAPI, HTTPException


class CrudsAnimeInfo:
    def __init__(self, db) -> None:
        self.db: Session = db
        pass

    """
    animenfoテーブル
    """

    def get_by_animeId(self, anime_id: str) -> Union[mylist_model.AnimeInfo, None]:
        return self.db.query(mylist_model.AnimeInfo).filter(mylist_model.AnimeInfo.anime_id == anime_id).first()

    def create(self, anime_info: mylist_model.AnimeInfo) -> mylist_model.AnimeInfo:
        db_anime_info = mylist_model.AnimeInfo(
            anime_id=anime_info.anime_id,
            title=anime_info.title,
            image=anime_info.image,
            url=anime_info.url,
            first=anime_info.first,
            stories=anime_info.stories,
        )
        self.db.add(db_anime_info)
        self.db.commit()
        self.db.refresh(db_anime_info)
        return db_anime_info

    def update(self, anime_info: mylist_model.AnimeInfo) -> mylist_model.AnimeInfo:
        db_anime_info = self.db.query(mylist_model.AnimeInfo).filter(
            mylist_model.AnimeInfo.anime_id == anime_info.anime_id
        )
        db_anime_info.update({mylist_model.AnimeInfo.stories: anime_info.stories})
        self.db.commit()
        return db_anime_info
