from fastapi import APIRouter
import schemas.mylist as mylist_schema
from models.mylist.scrape.scrape import Scrape

router = APIRouter()


@router.get("/my-list", response_model=mylist_schema.MyListGet)
async def mylist_get(id: str = None):
    result = Scrape().mylist(id)

    return mylist_schema.MyListGet(
        id=result["id"],
        d_anime_store_mylist_url=f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}",
        name=result["name"],
        mylist=result["mylist"],
    )
