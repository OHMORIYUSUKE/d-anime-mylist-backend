from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from .config import client, DANIME_MYLISTPAGE_BASE_URL, invalid_id_page, invalid_id_db, invalid_url, id

"""
例外テスト
"""

# POST

# id が不正(mylistが存在しない)
def test_post_invalid_url_1():
    response = client.post("/my-list", json={"url": f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={invalid_id_page}"})
    assert response.json()["detail"] == "mylist page not exist."
    assert response.status_code == 402


# urlが不正(d animeではない)
def test_post_invalid_url_2():
    response = client.post("/my-list", json={"url": invalid_url})
    assert response.json()["detail"] == "this url is not d-anime mylist page."
    assert response.status_code == 402


# 存在しているid
def test_post_invalid_url_3():
    response = client.post("/my-list", json={"url": f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}"})
    assert response.status_code == 409