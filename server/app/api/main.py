from app_setting import init_application
from routers import mylist


app = init_application()

app.include_router(mylist.router)
