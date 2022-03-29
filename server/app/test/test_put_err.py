from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from .config import client, DANIME_MYLISTPAGE_BASE_URL, invalid_id_page, invalid_id_db, invalid_url

"""
例外テスト
"""

# PUT

# id が不正(mylistが存在しない)
def test_put_invalid_url_1():
    response = client.put("/my-list", json={"url": f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={invalid_id_page}"})
    assert response.json()["detail"] == "mylist page not exist."
    assert response.status_code == 402


# id が不正(DBに存在しない)
def test_put_invalid_url_1():
    response = client.put("/my-list", json={"url": f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={invalid_id_db}"})
    assert response.json()["detail"] == "unknown mylist. you must register."
    assert response.status_code == 402


# urlが不正(d animeではない)
def test_put_invalid_url_2():
    response = client.put("/my-list", json={"url": invalid_url})
    assert response.json()["detail"] == "this url is not d-anime mylist page."
    assert response.status_code == 402
