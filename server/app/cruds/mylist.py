from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import FastAPI, HTTPException

import models.mylist as mylist_model
import schemas.mylist as mylist_schema


def get_mylist_by_id(db: Session, id: str):
    return (
        db.query(mylist_model.MylistContents)
        .filter(mylist_model.MylistContents.id == id)
        .first()
    )


def get_mylist_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(mylist_model.Mylists).offset(skip).limit(limit).all()


def create_mylist(db: Session, mylist: mylist_schema.MyListPost):
    db_mylist = mylist_model.Mylists(id=mylist.id, name=mylist.name)
    try:
        db.add(db_mylist)
        db.commit()
        db.refresh(db_mylist)
        return db_mylist
    except exc.IntegrityError:
        raise HTTPException(status_code=402, detail="this 'id' is already exists.")
