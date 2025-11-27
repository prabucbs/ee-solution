import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import json
from unittest.mock import patch
from app import app

client = app.test_client()

# -----------------------------
# Test 1: Successful gists fetch
# -----------------------------

@patch("requests.get")
def test_get_public_gists_ok(mock_get):
    # Mock the GitHub API response
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": "123",
            "description": "Test gist",
            "html_url": "https://gist.github.com/123",
            "files": {"file1.txt": {}}
        }
    ]

    res = client.get("/octocat?page=1&per_page=5")

    assert res.status_code == 200
    data = res.get_json()

    assert data["user"] == "octocat"
    assert data["count"] == 1
    assert data["gists"][0]["id"] == "123"


# -----------------------------
# Test 2: GitHub user not found
# -----------------------------

@patch("requests.get")
def test_user_not_found(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.text = "Not Found"

    res = client.get("/ghost")

    assert res.status_code == 404
    data = res.get_json()

    assert data["detail"] == "GitHub user not found"


# -----------------------------
# Test 3: Health check
# -----------------------------

def test_healthz():
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"