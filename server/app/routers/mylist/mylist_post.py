from fastapi import APIRouter

import schemas.mylist as mylist_schema

router = APIRouter()


@router.post("/my-list", response_model=mylist_schema.MyListPost)
async def mylist_post(my_list: mylist_schema.MyListPost):
    return mylist_schema.MyListPost(name=my_list.name, id=my_list.id)
