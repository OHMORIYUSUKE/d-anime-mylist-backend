from typing import TypeVar, Union
from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime

import models.mylist as mylist_model
import schemas.mylist as mylist_schema


class CrudsMylistContents:
    def __init__(self, db) -> None:
        self.db: Session = db
        pass

    """
    mylistContents テーブル
    """

    def get_by_mylistId(self, mylist_id: str, skip: int = 0, limit: int = 500) -> List[mylist_model.MylistContents]:
        return (
            self.db.query(mylist_model.MylistContents)
            .filter(mylist_model.MylistContents.mylist_id == mylist_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_mylistId_and_animeId(
        self, mylist_contents: mylist_model.MylistContents
    ) -> List[mylist_model.MylistContents]:
        return (
            self.db.query(mylist_model.MylistContents)
            .filter(
                mylist_model.MylistContents.mylist_id == mylist_contents.mylist_id,
                mylist_model.MylistContents.anime_id == mylist_contents.anime_id,
            )
            .first()
        )

    def create(
        self, mylist_contents: mylist_model.MylistContents
    ) -> Union[mylist_model.MylistContents, exc.IntegrityError]:
        db_mylist_content = mylist_model.MylistContents(
            mylist_id=mylist_contents.mylist_id, anime_id=mylist_contents.anime_id
        )
        try:
            self.db.add(db_mylist_content)
            self.db.commit()
            self.db.refresh(db_mylist_content)
            return db_mylist_content
        except exc.IntegrityError:
            return exc.IntegrityError

    def delete_by_mylistId_and_animeId(
        self, mylist_contents: mylist_model.MylistContents
    ) -> mylist_model.MylistContents:
        result = self.get_by_mylistId_and_animeId(mylist_contents=mylist_contents)
        dlete_data = (
            self.db.query(mylist_model.MylistContents)
            .filter(
                mylist_model.MylistContents.anime_id == mylist_contents.anime_id,
                mylist_model.MylistContents.mylist_id == mylist_contents.mylist_id,
            )
            .all()
        )
        self.db.delete(dlete_data)
        self.db.commit()
        return result

    def delete_by_mylistId(self, mylist_id: str) -> List[mylist_model.MylistContents]:
        result = self.get_by_mylistId(mylist_id=mylist_id)
        dlete_data = (
            self.db.query(mylist_model.MylistContents).filter(mylist_model.MylistContents.mylist_id == mylist_id).all()
        )
        self.db.delete(dlete_data)
        self.db.commit()
        return result
