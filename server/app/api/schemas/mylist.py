from datetime import datetime, time, timedelta
from pydantic import BaseModel, Field
from typing import List

# フロントエンド空受け取るデータ
class MyListPost(BaseModel):
    url: str = Field(..., description="dアニメストアのマイリストのURL")


# フロントエンドに返すデータ
class MylistContentResponseInfo(BaseModel):
    anime_id: str = Field(..., description="アニメのID")
    title: str = Field(..., description="アニメのタイトル")
    first: str = Field(..., description="第１話のタイトル")
    stories: str = Field(..., description="アニメの話数")
    image: str = Field(..., description="アニメのサムネイル画像のパス")
    url: str = Field(..., description="アニメの詳細ページ（d-anime ストアのページ）")


class MyListResponse(BaseModel):
    mylist_id: str = Field(..., description="マイリストのID")
    d_anime_store_url: str = Field(..., description="dアニメストアのマイリストのURL")
    created_at: datetime = Field(..., description="データが作成された時間")
    updated_at: datetime = Field(..., description="データが更新された時間")
    mylist: List[MylistContentResponseInfo] = Field(..., description="マイリストに登録されているアニメのリスト", max_item=500)


# crud用
class MyListContent(BaseModel):
    anime_id: str = Field(..., description="アニメのID")
    mylist_id: str = Field(..., description="マイリストのID")


class AnimeInfo(BaseModel):
    anime_id: str = Field(..., description="アニメのID")
    title: str = Field(..., description="アニメのタイトル")
    first: str = Field(..., description="第１話のタイトル")
    stories: str = Field(..., description="アニメの話数")
    image: str = Field(..., description="アニメのサムネイル画像のパス")
    url: str = Field(..., description="アニメの詳細ページ（d-anime ストアのページ）")


class MyListInfo(BaseModel):
    mylist_id: str = Field(..., description="マイリストのID")
    d_anime_store_url: str = Field(..., description="dアニメストアのマイリストのURL")
    created_at: datetime = Field(..., description="データが作成された時間")
    updated_at: datetime = Field(..., description="データが更新された時間")
