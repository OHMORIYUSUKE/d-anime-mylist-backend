from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from bs4 import ResultSet
import time

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
        stories_elm_list = []
        first_title_elm_list = []
        for link_elm in link_elm_list:
            next_soup = self.__get_html(link_elm.get("href"))
            first_title_elm_list.append(next_soup.find("span", class_="ui-clamp webkit2LineClamp"))

            stories_tmp = next_soup.find("div", class_="titleWrap")
            stories = " "
            try:
                stories = stories_tmp.h1.span.text
                print(stories_tmp.h1.span.text)
            except:
                pass
            stories_elm_list.append(stories)
            time.sleep(1)


        mylist_list: List[mylist_schema.MyListContent] = []
        for (title_elm, link_elm, image_elm, first_title_elm, stories_elm) in zip(title_elm_list, link_elm_list, image_elm_list, first_title_elm_list, stories_elm_list):
            mylist_list.append(
                mylist_schema.MyListContent(
                    title=title_elm.text, image=image_elm.get("data-src"), url=link_elm.get("href"), first=first_title_elm.text, stories=stories_elm
                )
            )

        if mylist_list == []:
            raise HTTPException(status_code=402, detail="mylist page not exist.")
        return mylist_list
