from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200, response.text

    response = client.delete(f"/activities/{activity_name}/participants/{email}")
    assert response.status_code == 200, response.text

    data = client.get("/activities").json()
    assert email not in data[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/participants/does-not-exist@mergington.edu")
    assert response.status_code == 404
