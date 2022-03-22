from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import FastAPI, HTTPException
from typing import List

import models.mylist as mylist_model
import schemas.mylist as mylist_schema
from service.get_id_in_url import get_id_in_url


def get_mylist_by_id(db: Session, id: str) -> mylist_schema.MyListGet:
    result = db.query(mylist_model.Mylists).filter(mylist_model.Mylists.id == id).first()
    if result == None:
        raise HTTPException(status_code=402, detail="unknown mylist. you must register.")
    return result


def get_mylist_contents_by_id(
    db: Session, id: str, skip: int = 0, limit: int = 500
) -> List[mylist_model.MylistContents]:
    return (
        db.query(mylist_model.MylistContents)
        .filter(mylist_model.MylistContents.id == id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_mylist_all(db: Session, skip: int = 0, limit: int = 100) -> List[mylist_schema.MyListPost]:
    return db.query(mylist_model.Mylists).offset(skip).limit(limit).all()


def create_mylist(db: Session, mylist: mylist_schema.MyListPost) -> mylist_model.Mylists:
    id = get_id_in_url(mylist.url)
    db_mylist = mylist_model.Mylists(id=id)
    try:
        db.add(db_mylist)
        db.commit()
        db.refresh(db_mylist)
        return db_mylist
    except exc.IntegrityError:
        raise HTTPException(status_code=402, detail="this mylist is already exists.")


def create_mylist_contents(
    db: Session, mylist_content: mylist_schema.MyListContent, id: str
) -> mylist_model.MylistContents:
    db_mylist_content = mylist_model.MylistContents(
        id=id,
        title=mylist_content.title,
        image=mylist_content.image,
        url=mylist_content.url,
    )
    try:
        db.add(db_mylist_content)
        db.commit()
        db.refresh(db_mylist_content)
        return db_mylist_content
    except exc.IntegrityError:
        raise HTTPException(status_code=402, detail="mylist is already exists")
