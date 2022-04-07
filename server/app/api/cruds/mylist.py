from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime

import models.mylist as mylist_model
import schemas.mylist as mylist_schema
from models.mylist import Mylists
from service.get_id_in_url import get_id_in_url

from service.scrape import Scrape


def get_mylist_by_id(db: Session, id: str) -> mylist_schema.MyListResponse:
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


def get_mylist_all(db: Session, skip: int = 0, limit: int = 10000) -> List[mylist_model.Mylists]:
    return db.query(mylist_model.Mylists).offset(skip).limit(limit).all()


def create_mylist(db: Session, mylist: mylist_schema.MyListPost) -> mylist_model.Mylists:
    id = get_id_in_url(url=mylist.url, param_name="shareListId")
    db_mylist = mylist_model.Mylists(mylist_id=id)
    try:
        db.add(db_mylist)
        db.commit()
        db.refresh(db_mylist)
        return db_mylist
    except exc.IntegrityError:
        raise HTTPException(status_code=402, detail="this mylist is already exists.")


def create_mylist_contents(
    db: Session, mylist_content_list: List[mylist_schema.MyListContent], id: str
) -> List[mylist_schema.MyListContent]:
    for mylist_content in mylist_content_list:
        db_mylist_content = mylist_model.MylistContents(
            mylist_id=id, title=mylist_content.title, anime_id=mylist_content.id
        )
        try:
            db.add(db_mylist_content)
            db.commit()
            db.refresh(db_mylist_content)
        except exc.IntegrityError:
            raise HTTPException(status_code=402, detail="this mylist is already exists.")
    return mylist_content_list


def update_mylist_contents(
    db: Session, mylist: mylist_schema.MyListPost, mylist_content_list: List[mylist_schema.MyListContent]
) -> List[mylist_model.MylistContents]:
    id = get_id_in_url(url=mylist.url, param_name="shareListId")
    # deleat
    dlete_data = db.query(mylist_model.MylistContents).filter(mylist_model.MylistContents.id == id).all()
    for dlete_data in dlete_data:
        db.delete(dlete_data)
        db.commit()
    # create
    mylist_contents_list = create_mylist_contents(db=db, mylist_content_list=mylist_content_list, id=id)
    return mylist_contents_list


def update_mylist(db: Session, mylist: mylist_schema.MyListPost) -> mylist_schema.MyListContent:
    id = get_id_in_url(url=mylist.url, param_name="shareListId")
    # select(不正にupdateさせない)(updateしたカラムを返す)
    result = db.query(mylist_model.Mylists).filter(mylist_model.Mylists.id == id).first()
    if result == None:
        raise HTTPException(status_code=402, detail="unknown mylist. you must register.")
    # update
    db_mylist = db.query(mylist_model.Mylists).filter(mylist_model.Mylists.id == id)
    db_mylist.update({mylist_model.Mylists.id: id, mylist_model.Mylists.updated_at: datetime.now()})
    db.commit()
    return result


def create_anime_info(
    db: Session, mylist_content_list: List[mylist_schema.MyListContent]
) -> List[mylist_schema.AnimeInfo]:
    response_list = []
    for mylist_content in mylist_content_list:
        # アニメ情報をスクレイピング
        anime_info = Scrape().anime_info(mylist_content.id)
        db_mylist_content = mylist_model.AnimeInfo(
            title=mylist_content.title,
            anime_id=mylist_content.id,
            image=anime_info.image,
            url=anime_info.url,
            first=anime_info.first,
            stories=anime_info.stories,
        )
        # スキーマ
        response_list.append(
            mylist_schema.AnimeInfo(
                id=mylist_content.id,
                title=mylist_content.title,
                anime_id=mylist_content.id,
                image=anime_info.image,
                url=anime_info.url,
                first=anime_info.first,
                stories=anime_info.stories,
            )
        )
        try:
            db.add(db_mylist_content)
            db.commit()
            db.refresh(db_mylist_content)
        except exc.IntegrityError:
            raise HTTPException(status_code=402, detail="this mylist is already exists.")
    return response_list
