from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


class Scrape:
    def __init__(self):
        pass

    def mylist(self, id):
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

        mylist_list = []
        for (title_elm, link_elm, image_elm) in zip(
            title_elm_list, link_elm_list, image_elm_list
        ):
            mylist_list.append(
                {
                    "title": title_elm.text,
                    "image": image_elm.get("data-src"),
                    "url": link_elm.get("href"),
                }
            )

        print(mylist_list)

        name = "Myマイリスト"

        return {"id": id, "name": name, "mylist": mylist_list}
