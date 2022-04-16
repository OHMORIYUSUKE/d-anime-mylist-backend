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


def get_mylist_all(db: Session) -> List[mylist_schema.MyListInfo]:
    mylist_all_list = CrudsMylist().get_mylist_all(db=db)
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
