import io
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_compare_endpoint_txt():
    files = {
        "file_old": ("old.txt", io.BytesIO(b"hello world"), "text/plain"),
        "file_new": ("new.txt", io.BytesIO(b"hello there"), "text/plain"),
    }
    response = client.post("/compare", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "-hello world" in data["diff"]
    assert "+hello there" in data["diff"]
    assert "Summary" in data["summary"]
