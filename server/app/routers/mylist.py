from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.db.db import SessionLocal
import schemas.mylist as mylist_schema
from service.scrape import Scrape
from cruds.mylist import create_mylist, get_mylist_by_id, get_mylist_all

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/my-list", response_model=mylist_schema.MyListGet)
async def mylist_get(id: str = None):
    result = Scrape().mylist(id)

    return mylist_schema.MyListGet(
        id=result["id"],
        d_anime_store_url=f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}",
        name=result["name"],
        mylist=result["mylist"],
    )


@router.post("/my-list", response_model=mylist_schema.MyListPost)
async def mylist_post(my_list: mylist_schema.MyListPost, db: Session = Depends(get_db)):
    res = create_mylist(db, my_list)
    return mylist_schema.MyListPost(name=my_list.name, id=my_list.id)
