from datetime import datetime, time, timedelta
from pydantic import BaseModel, Field
from typing import List


class MyListPost(BaseModel):
    url: str = Field(..., description="dアニメストアのマイリストのURL")


class MyListContent(BaseModel):
    title: str = Field(..., description="アニメのタイトル")
    image: str = Field(..., description="アニメのサムネイル画像のパス")
    url: str = Field(..., description="アニメの詳細ページ（d-anime ストアのページ）")


class MyListGet(BaseModel):
    id: str = Field(..., description="マイリストのID")
    d_anime_store_url: str = Field(..., description="dアニメストアのマイリストのURL")
    created_at: datetime = Field(..., description="データが作成された時間")
    updated_at: datetime = Field(..., description="データが更新された時間")
    mylist: List[MyListContent] = Field(..., description="マイリストに登録されているアニメのリスト", max_item=500)


class MyListInfo(BaseModel):
    id: str = Field(..., description="マイリストのID")
    d_anime_store_url: str = Field(..., description="dアニメストアのマイページのURL")
    created_at: datetime = Field(..., description="データが作成された時間")
    updated_at: datetime = Field(..., description="データが更新された時間")
