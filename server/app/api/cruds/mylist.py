from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime

import models.mylist as mylist_model
import schemas.mylist as mylist_schema

"""
mylist テーブル
"""


def get_mylist_by_mylistId(db: Session, mylist_id: mylist_schema.MylistId) -> mylist_model.Mylist:
    result = db.query(mylist_model.Mylist).filter(mylist_model.Mylist.mylist_id == mylist_id).first()
    if result == None:
        raise HTTPException(status_code=402, detail="unknown mylist. you must register.")
    return result


def create_mylist(db: Session, mylist_id: mylist_schema.MylistId) -> mylist_model.Mylist:
    db_mylist = mylist_model.Mylist(mylist_id=mylist_id.mylist_id)
    try:
        db.add(db_mylist)
        db.commit()
        db.refresh(db_mylist)
        return db_mylist
    except exc.IntegrityError:
        raise HTTPException(status_code=409, detail="this mylist is already exists.")


def update_mylist(db: Session, mylist_id: mylist_schema.MylistId) -> mylist_model.Mylist:
    db_mylist = db.query(mylist_model.Mylist).filter(mylist_model.Mylist.mylist_id == mylist_id.mylist_id)
    db_mylist.update(
        {mylist_model.Mylist.mylist_id: mylist_id.mylist_id, mylist_model.Mylist.updated_at: datetime.now()}
    )
    db.commit()
    return get_mylist_by_mylistId(db=db, mylist_id=mylist_id)


def get_mylist_all(db: Session, skip: int = 0, limit: int = 10000) -> List[mylist_model.Mylist]:
    return db.query(mylist_model.Mylist).offset(skip).limit(limit).all()


"""
mylistContents テーブル
"""


def get_mylistContents_by_mylistId(
    db: Session, mylist_id: mylist_schema.MylistId, skip: int = 0, limit: int = 500
) -> List[mylist_model.MylistContents]:
    return (
        db.query(mylist_model.MylistContents)
        .filter(mylist_model.MylistContents.mylist_id == mylist_id.mylist_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_mylistContents_by_mylistId_and_animeId(
    db: Session, mylist_contents: mylist_model.MylistContents
) -> List[mylist_model.MylistContents]:
    return (
        db.query(mylist_model.MylistContents)
        .filter(
            mylist_model.MylistContents.mylist_id == mylist_contents.mylist_id,
            mylist_model.MylistContents.anime_id == mylist_contents.anime_id,
        )
        .first()
    )


def create_mylistContents(db: Session, mylist_contents: mylist_model.MylistContents) -> mylist_model.MylistContents:
    db_mylist_content = mylist_model.MylistContents(
        mylist_id=mylist_contents.mylist_id, anime_id=mylist_contents.anime_id
    )
    db.add(db_mylist_content)
    db.commit()
    db.refresh(db_mylist_content)
    return db_mylist_content


def delete_mylistContents_by_mylistId_and_animeId(
    db: Session, mylist_contents: mylist_model.MylistContents
) -> mylist_model.MylistContents:
    result = get_mylistContents_by_mylistId_and_animeId(db=db, mylist_contents=mylist_contents)
    dlete_data = (
        db.query(mylist_model.MylistContents)
        .filter(
            mylist_model.MylistContents.anime_id == mylist_contents.anime_id,
            mylist_model.MylistContents.mylist_id == mylist_contents.mylist_id,
        )
        .all()
    )
    db.delete(dlete_data)
    db.commit()
    return result


def delete_mylistContents_by_mylistId(
    db: Session, mylist_id: mylist_schema.MylistId
) -> List[mylist_model.MylistContents]:
    result = get_mylistContents_by_mylistId(db=db, mylist_id=mylist_id)
    dlete_data = (
        db.query(mylist_model.MylistContents).filter(mylist_model.MylistContents.mylist_id == mylist_id.mylist_id).all()
    )
    db.delete(dlete_data)
    db.commit()
    return result


"""
animenfoテーブル
"""


def get_animeInfo_by_animeId(db: Session, anime_id: mylist_schema.AnimeId) -> List[mylist_model.AnimeInfo]:
    return db.query(mylist_model.AnimeInfo).filter(mylist_model.AnimeInfo.anime_id == anime_id.anime_id).first()


def create_animeInfo(db: Session, anime_info: mylist_model.AnimeInfo) -> mylist_model.AnimeInfo:
    db_anime_info = mylist_model.AnimeInfo(anime_info)
    db.add(db_anime_info)
    db.commit()
    db.refresh(db_anime_info)
    return db_anime_info


def update_animeInfo(db: Session, anime_info: mylist_model.AnimeInfo) -> mylist_model.AnimeInfo:
    db_anime_info = db.query(mylist_model.AnimeInfo).filter(mylist_model.AnimeInfo.anime_id == anime_info.anime_id)
    db_anime_info.update({mylist_model.AnimeInfo.stories: anime_info.stories})
    db.commit()
    return db_anime_info
