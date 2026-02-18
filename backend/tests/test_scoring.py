from app.ml.scoring import ChurnModel, FraudModel
from app.ml.features import extract_user_features


def _make_churn_events():
    events = []
    for i in range(20):
        events.append({"timestamp": f"2025-06-{1+i:02d}T10:00:00", "event_type": "page_view", "properties": '{"page": "/pricing"}'})
    for i in range(5):
        events.append({"timestamp": f"2025-06-{22+i:02d}T10:00:00", "event_type": "error", "properties": '{"code": "500"}'})
    return events


def _make_normal_events():
    events = []
    for i in range(30):
        events.append({"timestamp": f"2025-06-{1+(i%28):02d}T10:00:00", "event_type": "login", "properties": "{}"})
        events.append({"timestamp": f"2025-06-{1+(i%28):02d}T10:05:00", "event_type": "feature_use", "properties": '{"feature": "export"}'})
    return events


def test_churn_model_predict():
    model = ChurnModel()
    training_data = [
        (extract_user_features(_make_churn_events()), 1),
        (extract_user_features(_make_normal_events()), 0),
    ] * 10
    features_list = [f for f, _ in training_data]
    labels = [l for _, l in training_data]
    model.train(features_list, labels)

    score = model.predict(extract_user_features(_make_churn_events()))
    assert 0 <= score["score"] <= 100
    assert len(score["top_features"]) > 0
    assert isinstance(score["explanation"], str)


def test_fraud_model_predict():
    model = FraudModel()
    features = [extract_user_features(_make_normal_events())] * 20
    model.train(features)

    anomaly_features = extract_user_features(_make_churn_events())
    score = model.predict(anomaly_features)
    assert 0 <= score["score"] <= 100
