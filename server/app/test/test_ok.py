from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from .config import client, DANIME_MYLISTPAGE_BASE_URL, invalid_id_page, invalid_id_db, invalid_url, id

"""
正常(200)
"""


def test_post():
    response = client.post("/my-list", json={"url": f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}"})
    assert response.status_code == 200


def test_put():
    response = client.put("/my-list", json={"url": f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}"})
    assert response.json()["created_at"] < response.json()["updated_at"]
    assert response.status_code == 200


def test_get_by_id():
    response = client.get(f"/my-list?id={id}")
    assert response.status_code == 200


def test_get_all():
    response = client.get("/my-list/all")
    assert response.status_code == 200
