from datetime import datetime, time, timedelta
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
    d_anime_store_url: str
    name: str
    created_at: datetime
    mylist: List[MyListContent]
