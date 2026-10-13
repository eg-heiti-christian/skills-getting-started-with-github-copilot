from uuid import uuid4

from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant_aaa():
    # Arrange
    activity_name = "Chess Club"
    email = f"student-{uuid4().hex}@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert signup_response.status_code == 200, signup_response.text
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

    # Act
    delete_response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert delete_response.status_code == 200, delete_response.text
    remaining_activities = client.get("/activities").json()
    assert email not in remaining_activities[activity_name]["participants"]


def test_duplicate_signup_returns_400_aaa():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400, response.text
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_missing_activity_signup_returns_404_aaa():
    # Arrange
    activity_name = "Unknown Club"
    email = f"student-{uuid4().hex}@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404_aaa():
    # Arrange
    activity_name = "Chess Club"
    email = f"missing-{uuid4().hex}@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Participant not found in this activity"
