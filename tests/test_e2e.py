"""End-to-end smoke tests. Run with backend up: python -m pytest tests/test_e2e.py -v"""
import requests

BASE = "http://localhost:8000/api"


def test_health():
    assert requests.get(f"{BASE}/health").status_code == 200


def test_users_list():
    r = requests.get(f"{BASE}/users")
    assert r.status_code == 200
    users = r.json()
    assert len(users) == 50


def test_user_detail():
    users = requests.get(f"{BASE}/users").json()
    uid = users[0]["user_id"]
    r = requests.get(f"{BASE}/users/{uid}")
    assert r.status_code == 200
    assert "risk_scores" in r.json()


def test_timeline():
    users = requests.get(f"{BASE}/users").json()
    uid = users[0]["user_id"]
    r = requests.get(f"{BASE}/users/{uid}/timeline")
    assert r.status_code == 200
    assert "events" in r.json()


def test_clusters():
    r = requests.get(f"{BASE}/insights/clusters")
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_stats():
    r = requests.get(f"{BASE}/stats/overview")
    data = r.json()
    assert data["total_users"] == 50
    assert data["cluster_count"] == 3
