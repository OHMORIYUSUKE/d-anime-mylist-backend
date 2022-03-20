from fastapi import APIRouter
import schemas.mylist as mylist_schema
from service.scrape import Scrape

router = APIRouter()


@router.get("/my-list", response_model=mylist_schema.MyListGet)
async def mylist_get(id: str = None):
    result = Scrape().mylist(id)

    return mylist_schema.MyListGet(
        id=result["id"],
        d_anime_store_url=f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}",
        name=result["name"],
        mylist=result["mylist"],
    )


@router.post("/my-list", response_model=mylist_schema.MyListPost)
async def mylist_post(my_list: mylist_schema.MyListPost):
    return mylist_schema.MyListPost(name=my_list.name, id=my_list.id)
