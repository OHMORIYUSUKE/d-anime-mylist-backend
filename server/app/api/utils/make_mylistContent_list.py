import schemas.mylist as mylist_schema
import models.mylist as mylist_model
from schemas.mylist import MyListContent
from typing import List


def make_mylistContent_list(mylist_list_in_id: List[mylist_model.MylistContents]) -> List[mylist_schema.MyListContent]:
    mylist_list: List[mylist_schema.MyListContent] = []
    for mylist in mylist_list_in_id:
        mylist_list.append(
            mylist_schema.MyListContent(
                title=mylist.title, image=mylist.image, url=mylist.url, stories=mylist.stories, first=mylist.first
            )
        )
    return mylist_list
