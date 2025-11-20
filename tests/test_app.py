import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_signup_and_unregister():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"

    # Sign up
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert f"Signed up {email}" in signup_resp.json()["message"]

    # Duplicate signup should fail
    dup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert dup_resp.status_code == 400
    assert "already signed up" in dup_resp.json()["detail"]

    # Unregister
    unreg_resp = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unreg_resp.status_code == 200
    assert f"Unregistered {email}" in unreg_resp.json()["message"]

    # Unregister again should fail
    unreg_again = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unreg_again.status_code == 400
    assert "not registered" in unreg_again.json()["detail"]
