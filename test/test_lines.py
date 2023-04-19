from fastapi.testclient import TestClient

from src.api.server import app

import json

client = TestClient(app)


def test_get_line():
    response = client.get("/lines/7086")
    assert response.status_code == 200

    with open("test/lines/7086.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_conversation():
    response = client.get("/conservations/2")
    assert response.status_code == 200

    with open("test/conversations/2.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_lines():
    response = client.get("/lines/")
    assert response.status_code == 200

    with open("test/lines/root.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)

def test_get_line2():
    response = client.get("/lines/49")
    assert response.status_code == 200

    with open("test/lines/49.json", encoding="utf-8") as f:
        assert response.json() == json.load(f)


def test_404():
    response = client.get("/lines/400")
    assert response.status_code == 404
