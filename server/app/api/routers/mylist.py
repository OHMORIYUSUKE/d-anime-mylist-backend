from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import schemas.mylist as mylist_schema
from utils.scrape import Scrape
from utils.get_id_in_url import get_id_in_url
from service.mylist import (
    get_mylist_all,
)
import models.mylist as mylist_model
from typing import List
from utils.const_values import DANIME_MYLISTPAGE_BASE_URL

router = APIRouter()


# @router.put("/my-list", response_model=mylist_schema.MyList)
# async def create_item(mylist: mylist_schema.MyListPost, db: Session = Depends(get_db)):
#     id = get_id_in_url(url=mylist.url, param_name="shareListId")
#     mylist_info = get_mylist_by_id(db=db, mylist_id=id)
#     mylist_content_list: List[mylist_schema.MyListContents] = Scrape().mylist(id)
#     update_mylist(db=db, mylist=mylist)
#     update_mylist_contents(db=db, mylist=mylist, mylist_content_list=mylist_content_list)
#     mylist_content_anime_info_list = create_anime_info(db=db, mylist_content_list=mylist_content_list)
#     return mylist_schema.MyListResponse(
#         mylist_id=id,
#         d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}",
#         created_at=mylist_info.created_at,
#         updated_at=mylist_info.updated_at,
#         mylist=mylist_content_anime_info_list,
#     )


@router.get("/my-list/all", response_model=List[mylist_schema.MyListInfo])
async def mylist_get_all(db: Session = Depends(get_db)):
    return get_mylist_all(db=db)


# @router.get("/my-list", response_model=mylist_schema.MyListResponse)
# async def mylist_get(id: str = None, db: Session = Depends(get_db)):
#     mylist_info = get_mylist_by_id(db=db, mylist_id=id)
#     mylist_content_list = get_mylist_contents_by_id(db=db, mylist_id=id)
#     return mylist_schema.MyListResponse(
#         mylist_id=id,
#         d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}",
#         created_at=mylist_info.created_at,
#         updated_at=mylist_info.updated_at,
#         mylist=mylist_content_list,
#     )


# @router.post("/my-list", response_model=mylist_schema.MyListResponse)
# async def mylist_post(mylist: mylist_schema.MyListPost, db: Session = Depends(get_db)):
#     id = get_id_in_url(url=mylist.url, param_name="shareListId")
#     mylist_content_list: List[mylist_schema.MyListContents] = Scrape().mylist(id)
#     mylist_info = create_mylist(db=db, mylist=mylist)
#     mylist_list = create_mylist_contents(db=db, mylist_content_list=mylist_content_list, id=id)
#     mylist_animeinfo_list = create_anime_info(db=db, mylist_content_list=mylist_list)
#     return mylist_schema.MyListResponse(
#         mylist_id=id,
#         d_anime_store_url=f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}",
#         created_at=mylist_info.created_at,
#         updated_at=mylist_info.updated_at,
#         mylist=mylist_animeinfo_list,
#     )
