from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import schemas.mylist as mylist_schema
from schemas.mylist import MyListResponse, MyListPost
from service.scrape import Scrape
from service.get_id_in_url import get_id_in_url
from cruds.mylist import (
    create_mylist,
    get_mylist_by_id,
    get_mylist_all,
    get_mylist_contents_by_id,
    create_mylist_contents,
    update_mylist,
    update_mylist_contents,
    create_anime_info,
)
import models.mylist as mylist_model
from typing import List
from utils.const_values import DANIME_MYLISTPAGE_BASE_URL

router = APIRouter()

# TODO
@router.put("/my-list", response_model=mylist_schema.MyListResponse)
async def create_item(mylist: mylist_schema.MyListPost, db: Session = Depends(get_db)):
    id = get_id_in_url(url=mylist.url, param_name="shareListId")
    mylist_content_list: List[mylist_schema.MyListContent] = Scrape().mylist(id)
    mylist_info = update_mylist(db=db, mylist=mylist)
    update_mylist_contents_list = update_mylist_contents(db=db, mylist=mylist, mylist_content_list=mylist_content_list)
    mylist_content_anime_info_list = get_mylist_contents_by_id(db=db, mylist_id=id)
    return mylist_schema.MyListResponse(
        mylist_id=id,
        d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}",
        created_at=mylist_info.created_at,
        updated_at=mylist_info.updated_at,
        mylist=mylist_content_anime_info_list,
    )


@router.get("/my-list/all", response_model=List[mylist_schema.MyListInfo])
async def mylist_get_all(db: Session = Depends(get_db)):
    all_mylist_info_list: List[mylist_model.Mylists] = get_mylist_all(db=db)
    list_data: List[mylist_schema.MyListInfo] = []
    for data in all_mylist_info_list:
        list_data.append(
            mylist_schema.MyListInfo(
                mylist_id=data.mylist_id,
                d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={data.mylist_id}",
                created_at=data.created_at,
                updated_at=data.updated_at,
            )
        )
    return list_data


@router.get("/my-list", response_model=mylist_schema.MyListResponse)
async def mylist_get(id: str = None, db: Session = Depends(get_db)):
    mylist_info = get_mylist_by_id(db=db, mylist_id=id)
    mylist_content_list = get_mylist_contents_by_id(db=db, mylist_id=id)
    return mylist_schema.MyListResponse(
        mylist_id=id,
        d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}",
        created_at=mylist_info.created_at,
        updated_at=mylist_info.updated_at,
        mylist=mylist_content_list,
    )


# TODO
# AnimeInfoがDBにある場合はDBから取得する
@router.post("/my-list", response_model=mylist_schema.MyListResponse)
async def mylist_post(mylist: mylist_schema.MyListPost, db: Session = Depends(get_db)):
    id = get_id_in_url(url=mylist.url, param_name="shareListId")
    mylist_info = create_mylist(db=db, mylist=mylist)
    mylist_content_list: List[mylist_schema.MyListContent] = Scrape().mylist(id)
    mylist_list = create_mylist_contents(db=db, mylist_content_list=mylist_content_list, id=id)
    mylist_animeinfo_list = create_anime_info(db=db, mylist_content_list=mylist_list)
    return mylist_schema.MyListResponse(
        mylist_id=id,
        d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}",
        created_at=mylist_info.created_at,
        updated_at=mylist_info.updated_at,
        mylist=mylist_animeinfo_list,
    )
