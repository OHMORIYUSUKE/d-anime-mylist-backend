from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.db.db import SessionLocal
import schemas.mylist as mylist_schema
from service.scrape import Scrape
from cruds.mylist import (
    create_mylist,
    get_mylist_by_id,
    get_mylist_all,
    get_mylist_contents_by_id,
)

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
    mylist = Scrape().mylist(id)

    mylist_info: mylist_schema.MyListGet = get_mylist_by_id(db, id)

    return mylist_schema.MyListGet(
        id=id,
        d_anime_store_url=f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}",
        name=mylist_info.name,
        created_at=mylist_info.created_at,
        mylist=mylist,
    )


@router.post("/my-list", response_model=mylist_schema.MyListPost)
async def mylist_post(my_list: mylist_schema.MyListPost, db: Session = Depends(get_db)):
    res = create_mylist(db, my_list)
    return mylist_schema.MyListPost(name=my_list.name, id=my_list.id)
