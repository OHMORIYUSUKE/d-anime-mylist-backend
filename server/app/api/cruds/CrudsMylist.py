from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime

import models.mylist as mylist_model
import schemas.mylist as mylist_schema


class CrudsMylist:
    def __init__(self) -> None:
        pass

    """
    mylist テーブル
    """

    def get_by_mylistId(self, db: Session, mylist_id: str) -> mylist_model.Mylist:
        result = db.query(mylist_model.Mylist).filter(mylist_model.Mylist.mylist_id == mylist_id).first()
        if result == None:
            raise HTTPException(status_code=402, detail="unknown mylist. you must register.")
        return result

    def create(self, db: Session, mylist_id: str) -> mylist_model.Mylist:
        db_mylist = mylist_model.Mylist(mylist_id=mylist_id)
        try:
            db.add(db_mylist)
            db.commit()
            db.refresh(db_mylist)
            return db_mylist
        except exc.IntegrityError:
            raise HTTPException(status_code=409, detail="this mylist is already exists.")

    def update(self, db: Session, mylist_id: str) -> mylist_model.Mylist:
        db_mylist = db.query(mylist_model.Mylist).filter(mylist_model.Mylist.mylist_id == mylist_id)
        db_mylist.update({mylist_model.Mylist.mylist_id: mylist_id, mylist_model.Mylist.updated_at: datetime.now()})
        db.commit()
        return self.get_by_mylistId(db=db, mylist_id=mylist_id)

    def get_mylist_all(self, db: Session, skip: int = 0, limit: int = 10000) -> List[mylist_model.Mylist]:
        return db.query(mylist_model.Mylist).offset(skip).limit(limit).all()
