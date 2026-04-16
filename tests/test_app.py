from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_root_redirects_to_static_index():
    response = client.get("/")
    assert response.status_code == 200
    assert str(response.url).endswith("/static/index.html")
    assert "Mergington High School" in response.text or response.headers.get("content-type")


def test_get_activities_returns_activity_list():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"], dict)


def test_signup_for_activity_adds_participant():
    email = "test.student@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}


def test_signup_for_activity_returns_400_if_already_signed_up():
    email = "existing.student@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})

    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_missing_activity_returns_404():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_from_activity():
    email = "remove.student@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})

    response = client.delete("/activities/Chess Club/participants", params={"email": email})
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}


def test_remove_missing_participant_returns_404():
    response = client.delete("/activities/Chess Club/participants", params={"email": "unknown@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "unknown@mergington.edu is not signed up for Chess Club"
