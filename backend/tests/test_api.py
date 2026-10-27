"""
Integration tests for FastAPI endpoints.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "UP"
    assert "hadoop_mapreduce" in data["features"]

def test_list_datasets():
    response = client.get("/api/datasets")
    assert response.status_code == 200
    data = response.json()
    assert "datasets" in data
    assert len(data["datasets"]) > 0

def test_analytics_overview():
    response = client.get("/api/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert "total_records" in data
    assert "sentiment_percentages" in data
    assert "unique_words" in data
    assert "sdg_alignment" in data

def test_mapreduce_jobs_endpoint():
    response = client.get("/api/mapreduce/jobs")
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    assert len(data["jobs"]) == 5

def test_records_pagination_and_filter():
    response = client.get("/api/analytics/records?page=1&page_size=5&sentiment=all")
    assert response.status_code == 200
    data = response.json()
    assert "records" in data
    assert len(data["records"]) <= 5
    assert data["total_records"] > 0
