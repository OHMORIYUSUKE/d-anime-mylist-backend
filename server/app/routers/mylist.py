from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.db.db import SessionLocal
import schemas.mylist as mylist_schema
from schemas.mylist import MyListContent
from service.scrape import Scrape
from service.get_id_in_url import get_id_in_url
from cruds.mylist import (
    create_mylist,
    get_mylist_by_id,
    get_mylist_all,
    get_mylist_contents_by_id,
    create_mylist_contents,
)
import models.mylist as mylist_model
from typing import List
from utils.make_mylistContent_list import make_mylistContent_list

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/my-list", response_model=mylist_schema.MyListGet)
async def mylist_get(id: str = None, db: Session = Depends(get_db)):
    mylist_info: mylist_schema.MyListGet = get_mylist_by_id(db=db, id=id)
    mylist_list_in_id: List[mylist_model.MylistContents] = get_mylist_contents_by_id(db=db, id=id)

    mylist_list: List[mylist_schema.MyListContent] = make_mylistContent_list(mylist_list_in_id=mylist_list_in_id)

    return mylist_schema.MyListGet(
        id=id,
        d_anime_store_url=f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}",
        created_at=mylist_info.created_at,
        updated_at=mylist_info.updated_at,
        mylist=mylist_list,
    )


@router.post("/my-list", response_model=mylist_schema.MyListGet)
async def mylist_post(mylist: mylist_schema.MyListPost, db: Session = Depends(get_db)):
    res = create_mylist(db=db, mylist=mylist)
    # スクレイピング
    id = get_id_in_url(mylist.url)
    mylist_list: List[mylist_schema.MyListContent] = Scrape().mylist(id)
    for mylist_content in mylist_list:
        create_mylist_contents(db=db, mylist_content=mylist_content, id=id)
    # DB空mylistの情報を取得
    mylist_info: mylist_schema.MyListGet = get_mylist_by_id(db=db, id=id)
    mylist_list_in_id: List[mylist_model.MylistContents] = get_mylist_contents_by_id(db=db, id=id)
    mylist_list: List[mylist_schema.MyListContent] = make_mylistContent_list(mylist_list_in_id=mylist_list_in_id)

    return mylist_schema.MyListGet(
        id=id,
        d_anime_store_url=f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}",
        created_at=mylist_info.created_at,
        updated_at=mylist_info.updated_at,
        mylist=mylist_list,
    )
