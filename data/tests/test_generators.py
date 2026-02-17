from generators.users import generate_users
from generators.events import generate_events_for_user
from generators.clusters import generate_clusters


def test_generate_users_count():
    users = generate_users(count=10, seed=42)
    assert len(users) == 10


def test_generate_users_scenario_distribution():
    users = generate_users(count=50, seed=42)
    tags = [u["scenario_tag"] for u in users]
    assert "churn" in tags
    assert "fraud" in tags
    assert "normal" in tags
    assert "confused" in tags


def test_generate_users_fields():
    users = generate_users(count=1, seed=42)
    u = users[0]
    assert all(k in u for k in ["user_id", "name", "email", "created_at", "account_type", "scenario_tag"])


def test_generate_events_churn_user():
    user = {
        "user_id": "test-churn-1",
        "created_at": "2025-06-01T00:00:00",
        "scenario_tag": "churn",
    }
    events = generate_events_for_user(user)
    assert len(events) > 20
    types = {e["event_type"] for e in events}
    assert "page_view" in types


def test_generate_events_fraud_user():
    user = {
        "user_id": "test-fraud-1",
        "created_at": "2025-06-01T00:00:00",
        "scenario_tag": "fraud",
    }
    events = generate_events_for_user(user)
    assert len(events) > 10
    types = {e["event_type"] for e in events}
    assert "payment" in types or "api_call" in types


def test_generate_clusters():
    clusters = generate_clusters()
    assert len(clusters) == 3
    assert all("cluster_id" in c for c in clusters)
    assert all("auto_summary" in c for c in clusters)
