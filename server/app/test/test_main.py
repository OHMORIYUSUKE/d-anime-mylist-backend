from fastapi.testclient import TestClient

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))

from main import app

client = TestClient(app)

id = "O10cMRZUU1Dj72JH"
DANIME_MYLISTPAGE_BASE_URL = "https://anime.dmkt-sp.jp/animestore/public_list"

def test_post_main():
    response = client.post("/my-list", json={"url": f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}"})
    assert response.status_code == 402

def test_put_main():
    response = client.put("/my-list", json={"url": f"{DANIME_MYLISTPAGE_BASE_URL}?shareListId={id}"})
    assert response.json()["created_at"] < response.json()["updated_at"]
    assert response.status_code == 200

def test_get_by_id_main():
    response = client.get(f"/my-list?id={id}")
    assert response.status_code == 200

def test_get_all_main():
    response = client.get("/my-list/all")
    assert response.status_code == 200