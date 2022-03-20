from turtle import title
from pydantic import BaseModel
from typing import List


class MyListPost(BaseModel):
    name: str
    id: str


class MyListContent(BaseModel):
    title: str
    image: str
    url: str


class MyListGet(BaseModel):
    id: str
    d_anime_store_mylist_url: str
    name: str
    mylist: List[MyListContent]
