from app.ml.features import extract_user_features


def test_extract_features_returns_dict():
    events = [
        {"timestamp": "2025-06-01T10:00:00", "event_type": "login", "properties": "{}"},
        {"timestamp": "2025-06-01T10:05:00", "event_type": "page_view", "properties": '{"page": "/pricing"}'},
        {"timestamp": "2025-06-01T10:10:00", "event_type": "error", "properties": '{"code": "500"}'},
    ]
    features = extract_user_features(events)
    assert isinstance(features, dict)
    assert "total_events" in features
    assert "error_rate" in features
    assert "pricing_page_views" in features
    assert features["total_events"] == 3
    assert features["error_rate"] > 0
    assert features["pricing_page_views"] == 1
