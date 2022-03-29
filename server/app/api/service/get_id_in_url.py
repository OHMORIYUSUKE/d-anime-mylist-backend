import urllib.parse
from fastapi import FastAPI, HTTPException


def get_id_in_url(url: str) -> str:
    urllib.parse.urlparse(url)
    qs = urllib.parse.urlparse(url).query
    qs_d = urllib.parse.parse_qs(qs)
    try:
        id = qs_d["shareListId"][0]
        return id
    except KeyError:
        raise HTTPException(status_code=402, detail="this url is not d-anime mylist page.")
