from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck():
    response = client.get("/")
    assert response.status_code == 200


def test_overview_unauthorized():
    today = date.today()
    response = client.get(f"/api/v1/analytics/overview?date_from={today - timedelta(days=7)}&date_to={today}")
    assert response.status_code == 401
