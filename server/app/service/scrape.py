from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import ResultSet

from fastapi import FastAPI, HTTPException

from typing import List
import schemas.mylist as mylist_schema


class Scrape:
    def __init__(self):
        pass

    def __get_html(self, url: str) -> BeautifulSoup:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome("chromedriver", options=options)
        driver.implicitly_wait(10)
        driver.get(url)
        html = driver.page_source.encode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def mylist(self, id: str) -> List[mylist_schema.MyListContent]:
        soup = self.__get_html(f"https://anime.dmkt-sp.jp/animestore/public_list?shareListId={id}")
        # print(soup.prettify())

        title_elm_list: List[ResultSet] = soup.find_all("span", class_="ui-clamp")
        image_elm_list: List[ResultSet] = soup.find_all("img")
        link_elm_list: List[ResultSet] = soup.find_all("a", class_="itemModuleIn")

        mylist_list: List[mylist_schema.MyListContent] = []
        for (title_elm, link_elm, image_elm) in zip(title_elm_list, link_elm_list, image_elm_list):
            mylist_list.append(
                {
                    "title": title_elm.text,
                    "image": image_elm.get("data-src"),
                    "url": link_elm.get("href"),
                }
            )

        if mylist_list == []:
            raise HTTPException(status_code=402, detail="mylist page not exist.")
        return mylist_list
