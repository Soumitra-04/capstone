from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_streams():
    response = client.get("/streams")
    assert response.status_code == 200
    assert isinstance(response.json(), list)