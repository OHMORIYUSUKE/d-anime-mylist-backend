from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import get_db
import schemas.mylist as mylist_schema
from service.mylist import Service
from typing import List

router = APIRouter()


@router.put("/my-list", response_model=mylist_schema.MyList)
async def create_item(post_data: mylist_schema.MyListPostPut, db: Session = Depends(get_db)):
    return Service(db=db).update_mylist(post_data=post_data)


@router.get("/my-list/all", response_model=List[mylist_schema.MyListInfo])
async def mylist_get_all(db: Session = Depends(get_db)):
    return Service(db=db).get_mylist_all()


@router.get("/my-list", response_model=mylist_schema.MyList)
async def mylist_get(id: str = None, db: Session = Depends(get_db)):
    return Service(db=db).get_mylist(mylist_id=id)


@router.post("/my-list", response_model=mylist_schema.MyList)
async def mylist_post(post_data: mylist_schema.MyListPostPut, db: Session = Depends(get_db)):
    return Service(db=db).create_mylist(post_data=post_data)
