from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime

import models.mylist as mylist_model
import schemas.mylist as mylist_schema
from models.mylist import Mylist
from utils.const_values import DANIME_MYLISTPAGE_BASE_URL
from utils.get_id_in_url import get_id_in_url

from utils.scrape import Scrape

from cruds.crudsMylist import CrudsMylist
from cruds.crudsMylistContents import CrudsMylistContents
from cruds.crudsAnimeInfo import CrudsAnimeInfo


class Service:
    def __init__(self, db: Session) -> None:
        self.db = db
        pass

    def get_mylist_all(self) -> List[mylist_schema.MyListInfo]:
        mylist_all_list = CrudsMylist(db=self.db).get_mylist_all()
        res = []
        for data in mylist_all_list:
            res.append(
                mylist_schema.MyListInfo(
                    mylist_id=data.mylist_id,
                    d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={data.mylist_id}",
                    created_at=data.created_at,
                    updated_at=data.updated_at,
                )
            )
        return res

    def get_mylist(self, mylist_id: str) -> mylist_schema.MyList:
        mylist_info = CrudsMylist(db=self.db).get_by_mylistId(mylist_id=mylist_id)
        mylist_contents_list = CrudsMylistContents(db=self.db).get_by_mylistId(mylist_id=mylist_id)
        anime_list = []
        for data in mylist_contents_list:
            anime_data = CrudsAnimeInfo(db=self.db).get_by_animeId(anime_id=data.anime_id)
            anime_list.append(
                mylist_schema.MylistContents(
                    anime_id=anime_data.anime_id,
                    title=anime_data.title,
                    first=anime_data.first,
                    stories=anime_data.stories,
                    image=anime_data.image,
                    url=anime_data.url,
                )
            )
        return mylist_schema.MyList(
            mylist_id=mylist_id,
            d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={mylist_id}",
            created_at=mylist_info.created_at,
            updated_at=mylist_info.updated_at,
            mylist=anime_list,
        )

    