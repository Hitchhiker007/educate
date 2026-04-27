from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_educate_returns_200():
    response = client.post("/educate", json={"code_snippet": "def hello(): pass"})
    assert response.status_code == 200

def test_educate_returns_correct_response_body():
    response = client.post("/educate", json={"code_snippet": "def hello(): pass"})
    data = response.json()
    assert "docs" in data and "summary" in data and "improvements" in data