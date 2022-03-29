from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from .config import client, DANIME_MYLISTPAGE_BASE_URL, invalid_id_page, invalid_id_db, invalid_url


"""
例外テスト
"""

# GET

# idが不正(DBに存在しない)
def test_get_by_invalid_id():
    response = client.get(f"/my-list?id={invalid_id_db}")
    assert response.json()["detail"] == "unknown mylist. you must register."
    assert response.status_code == 402


# idが不正(ページが存在しない)
def test_get_by_invalid_id():
    response = client.get(f"/my-list?id={invalid_id_page}")
    assert response.json()["detail"] == "unknown mylist. you must register."
    assert response.status_code == 402
