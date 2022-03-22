from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal
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
    update_mylist,
)
import models.mylist as mylist_model
from typing import List
from utils.make_mylistContent_list import make_mylistContent_list
from utils.const_values import D_ANIME_MYPAGE_BASE_URL

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.put("/my-list", response_model=mylist_schema.MyListInfo)
async def create_item(mylist: mylist_schema.MyListPost, db: Session = Depends(get_db)):
    id = get_id_in_url(mylist.url)
    update_mylist_res = update_mylist(db=db, mylist=mylist)
    mylist_list: List[mylist_schema.MyListContent] = Scrape().mylist(id)
    for mylist_content in mylist_list:
        create_mylist_contents_res = create_mylist_contents(db=db, mylist_content=mylist_content, id=id)
    return mylist_schema.MyListInfo(
        id=id,
        d_anime_store_url=mylist.url,
        created_at=update_mylist_res.created_at,
        updated_at=update_mylist_res.updated_at,
    )


@router.get("/my-list/all", response_model=List[mylist_schema.MyListInfo])
async def mylist_get_all(db: Session = Depends(get_db)):
    all_mylist_info_list: List[mylist_model.Mylists] = get_mylist_all(db=db)
    list_data: List[mylist_schema.MyListInfo] = []
    for data in all_mylist_info_list:
        list_data.append(
            mylist_schema.MyListInfo(
                id=data.id,
                d_anime_store_url=f"{D_ANIME_MYPAGE_BASE_URL}?shareListId={data.id}",
                created_at=data.created_at,
                updated_at=data.updated_at,
            )
        )
    return list_data


@router.get("/my-list", response_model=mylist_schema.MyListGet)
async def mylist_get(id: str = None, db: Session = Depends(get_db)):
    mylist_info: mylist_schema.MyListGet = get_mylist_by_id(db=db, id=id)
    mylist_list_in_id: List[mylist_model.MylistContents] = get_mylist_contents_by_id(db=db, id=id)
    mylist_list: List[mylist_schema.MyListContent] = make_mylistContent_list(mylist_list_in_id=mylist_list_in_id)
    return mylist_schema.MyListGet(
        id=id,
        d_anime_store_url=f"{D_ANIME_MYPAGE_BASE_URL}?shareListId={id}",
        created_at=mylist_info.created_at,
        updated_at=mylist_info.updated_at,
        mylist=mylist_list,
    )


@router.post("/my-list", response_model=mylist_schema.MyListGet)
async def mylist_post(mylist: mylist_schema.MyListPost, db: Session = Depends(get_db)):
    create_mylist_res = create_mylist(db=db, mylist=mylist)
    # スクレイピング
    id = get_id_in_url(mylist.url)
    mylist_list: List[mylist_schema.MyListContent] = Scrape().mylist(id)
    for mylist_content in mylist_list:
        create_mylist_contents_res = create_mylist_contents(db=db, mylist_content=mylist_content, id=id)
    # DB空mylistの情報を取得
    mylist_info: mylist_schema.MyListGet = get_mylist_by_id(db=db, id=id)
    mylist_list_in_id: List[mylist_model.MylistContents] = get_mylist_contents_by_id(db=db, id=id)
    mylist_list: List[mylist_schema.MyListContent] = make_mylistContent_list(mylist_list_in_id=mylist_list_in_id)
    return mylist_schema.MyListGet(
        id=id,
        d_anime_store_url=f"{D_ANIME_MYPAGE_BASE_URL}?shareListId={id}",
        created_at=mylist_info.created_at,
        updated_at=mylist_info.updated_at,
        mylist=mylist_list,
    )
