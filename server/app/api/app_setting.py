from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def init_application():
    app = FastAPI(
        title="d-anime-mylist",
        description="This is a d-anime-mylist API.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
