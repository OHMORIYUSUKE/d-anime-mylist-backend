from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

import json


def get_application():
    app = FastAPI(title="d-anime-mylist", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app = get_application()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/my-list/")
async def read_item(id: str = None):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome("chromedriver", options=options)
    driver.implicitly_wait(10)
    driver.get(f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}")
    html = driver.page_source.encode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())

    title_elm_list = soup.find_all("span", class_="ui-clamp")
    image_elm_list = soup.find_all("img")
    link_elm_list = soup.find_all("a", class_="itemModuleIn")

    title_list = [title.text for title in title_elm_list]
    image_list = [image.get("href") for image in image_elm_list]
    link_list = [link.get("data-src") for link in link_elm_list]

    mylist_list = [
        {"title": title, "image": image, "url": link}
        for (title, link, image) in zip(title_list, link_list, image_list)
    ]

    res = {
        "d-anime-store-mylist-url": f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}",
        "mylist": mylist_list,
    }
    return res
