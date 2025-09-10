import pytest
from fastapi.testclient import TestClient
from app.main import app
from io import BytesIO


client = TestClient(app)


class TestAPI:
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_contact_verification_endpoint(self):
        file_content = b"John Smith\nEmail: john@example.com\nPhone: (555) 123-4567"
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}

        response = client.post("/api/v1/verify/contact", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "risk_score" in data
        assert "confidence" in data

    def test_ai_content_analysis_endpoint(self):
        file_content = (
            b"I am an excellent team player with strong problem-solving abilities."
        )
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}

        response = client.post("/api/v1/analyze/content", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "overall_ai_probability" in data
        assert "confidence" in data

    def test_document_examination_endpoint(self):
        file_content = b"Test document content"
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}

        response = client.post("/api/v1/examine/document", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "risk_score" in data
        assert "authenticity_indicators" in data

    def test_full_fraud_detection_endpoint(self):
        file_content = b"John Smith\nEmail: john@tempmail.com\nPhone: (555) 123-4567\n\nI am an excellent team player."
        files = {"file": ("test.txt", BytesIO(file_content), "text/plain")}

        response = client.post("/api/v1/detect/resume", files=files)
        assert response.status_code == 200
        data = response.json()
        assert "overall_risk_score" in data
        assert "risk_level" in data
        assert "confidence" in data
        assert "detected_issues" in data
        assert "contact_verification" in data
        assert "ai_content_analysis" in data
        assert "document_analysis" in data

    def test_invalid_file_type(self):
        file_content = b"invalid content"
        files = {
            "file": ("test.exe", BytesIO(file_content), "application/octet-stream")
        }

        response = client.post("/api/v1/detect/resume", files=files)
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]

    def test_empty_file(self):
        files = {"file": ("test.txt", BytesIO(b""), "text/plain")}

        response = client.post("/api/v1/detect/resume", files=files)
        assert response.status_code == 400
        assert "Empty file" in response.json()["detail"]
