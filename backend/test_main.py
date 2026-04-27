from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

mock_response = MagicMock()
mock_response.text = '{"docs": ["test doc"], "summary": "test summary", "improvements": ["test improvement"]}'
    
def test_educate_returns_200():
    with patch("main.client.models.generate_content", return_value=mock_response):
        response = client.post("/educate", json={"code_snippet": "def hello(): pass"})
        assert response.status_code == 200

def test_educate_returns_correct_response_body():
    with patch("main.client.models.generate_content", return_value=mock_response):
        response = client.post("/educate", json={"code_snippet": "def hello(): pass"})
        data = response.json()
        assert "docs" in data and "summary" in data and "improvements" in data
    
