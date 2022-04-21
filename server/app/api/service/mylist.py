from sqlalchemy.orm import Session
from typing import List

import models.mylist as mylist_model
import schemas.mylist as mylist_schema
from utils.const_values import DANIME_MYLISTPAGE_BASE_URL
from utils.get_id_in_url import get_id_in_url
from utils.scrape import Scrape

from cruds.CrudsMylist import CrudsMylist
from cruds.CrudsMylistContents import CrudsMylistContents
from cruds.CrudsAnimeInfo import CrudsAnimeInfo


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

    def create_mylist(self, post_data: mylist_schema.MyListPostPut) -> mylist_schema.MyList:
        mylist_id = get_id_in_url(post_data.url, param_name="shareListId")
        mylist_list = Scrape().mylist(mylist_id=mylist_id)
        CrudsMylist(db=self.db).create(mylist_id=mylist_id)
        mylist_info = CrudsMylist(db=self.db).get_by_mylistId(mylist_id=mylist_id)
        anime_info_list = []
        for data in mylist_list:
            CrudsMylistContents(db=self.db).create(
                mylist_contents=mylist_model.MylistContents(mylist_id=mylist_id, anime_id=data.anime_id)
            )
            anime_info = self.__if_not_exist__create_anime_info__if_old_data__update_anime_info(anime_id=data.anime_id)
            anime_info_list.append(
                mylist_schema.MylistContents(
                    anime_id=anime_info.anime_id,
                    title=anime_info.title,
                    first=anime_info.first,
                    stories=anime_info.stories,
                    image=anime_info.image,
                    url=anime_info.url,
                )
            )
        return mylist_schema.MyList(
            mylist_id=mylist_id,
            d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={mylist_id}",
            created_at=mylist_info.created_at,
            updated_at=mylist_info.updated_at,
            mylist=anime_info_list,
        )

    def update_mylist(self, post_data: mylist_schema.MyListPostPut) -> mylist_schema.MyList:
        mylist_id = get_id_in_url(post_data.url, param_name="shareListId")
        mylist_info = CrudsMylist(db=self.db).get_by_mylistId(mylist_id=mylist_id)
        mylist_list = Scrape().mylist(mylist_id=mylist_id)
        CrudsMylist(db=self.db).update(mylist_id=mylist_id)
        CrudsMylistContents(db=self.db).delete_by_mylistId(mylist_id=mylist_id)
        anime_info_list = []
        for data in mylist_list:
            CrudsMylistContents(db=self.db).create(
                mylist_contents=mylist_model.MylistContents(mylist_id=mylist_id, anime_id=data.anime_id)
            )
            anime_info = self.__if_not_exist__create_anime_info__if_old_data__update_anime_info(anime_id=data.anime_id)
            anime_info_list.append(
                mylist_schema.MylistContents(
                    anime_id=anime_info.anime_id,
                    title=anime_info.title,
                    first=anime_info.first,
                    stories=anime_info.stories,
                    image=anime_info.image,
                    url=anime_info.url,
                )
            )
        return mylist_schema.MyList(
            mylist_id=mylist_id,
            d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={mylist_id}",
            created_at=mylist_info.created_at,
            updated_at=mylist_info.updated_at,
            mylist=anime_info_list,
        )

    def __if_not_exist__create_anime_info__if_old_data__update_anime_info(
        self, anime_id: str
    ) -> mylist_model.AnimeInfo:
        anime_info_from_db = CrudsAnimeInfo(db=self.db).get_by_animeId(anime_id=anime_id)
        if anime_info_from_db == None:
            anime_info = Scrape().anime_info(anime_id=anime_id)
            CrudsAnimeInfo(db=self.db).create(anime_info=anime_info)
            return anime_info
        elif anime_info_from_db.stories == " ":
            anime_info = Scrape().anime_info(anime_id=anime_id)
            CrudsAnimeInfo(db=self.db).update(anime_info=anime_info)
            return anime_info
        else:
            return anime_info_from_db
