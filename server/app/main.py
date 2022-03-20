from app_setting import init_application
from routers.mylist import mylist_get, mylist_post


app = init_application()

app.include_router(mylist_get.router)
app.include_router(mylist_post.router)
