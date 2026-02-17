import random
import uuid
import json
from datetime import datetime, timedelta

EVENT_TYPES = [
    "page_view", "api_call", "login", "payment", "support_ticket",
    "search", "feature_use", "error", "signup", "message_sent",
]

PAGES = ["/dashboard", "/settings", "/pricing", "/docs", "/billing", "/profile", "/features", "/integrations"]
FEATURES = ["export", "import", "webhook", "api-key", "team-invite", "sso", "analytics", "notifications"]
SEARCH_QUERIES_CONFUSED = [
    "how to export data", "export not working", "where is export button",
    "cant find export", "data export help", "download my data",
    "how to invite team", "team invite broken", "add team member",
    "where is team settings", "team management help",
]
SUPPORT_MESSAGES_CONFUSED = [
    "I can't find the export feature anywhere in the dashboard",
    "The export button seems to have disappeared after the update",
    "How do I download my data? I've looked everywhere",
    "Team invite link doesn't seem to work for my colleagues",
    "I'm trying to add a team member but the option is grayed out",
]


def generate_events_for_user(user: dict, seed: int = 42) -> list[dict]:
    rng = random.Random(seed + hash(user["user_id"]))
    created = datetime.fromisoformat(user["created_at"])
    scenario = user["scenario_tag"]

    if scenario == "churn":
        return _generate_churn_events(rng, user["user_id"], created)
    elif scenario == "fraud":
        return _generate_fraud_events(rng, user["user_id"], created)
    elif scenario == "confused":
        return _generate_confused_events(rng, user["user_id"], created)
    else:
        return _generate_normal_events(rng, user["user_id"], created)


def _generate_churn_events(rng, user_id, created):
    events = []
    for day in range(15):
        ts = created + timedelta(days=day, hours=rng.randint(8, 20))
        for _ in range(rng.randint(3, 8)):
            ts += timedelta(minutes=rng.randint(1, 30))
            events.append(_event(rng, user_id, ts, "page_view", {"page": rng.choice(PAGES)}))
            if rng.random() < 0.3:
                events.append(_event(rng, user_id, ts, "feature_use", {"feature": rng.choice(FEATURES)}))
    for day in range(15, 31):
        ts = created + timedelta(days=day, hours=rng.randint(8, 20))
        for _ in range(rng.randint(1, 4)):
            ts += timedelta(minutes=rng.randint(1, 30))
            if rng.random() < 0.4:
                events.append(_event(rng, user_id, ts, "page_view", {"page": "/pricing"}))
            if rng.random() < 0.3:
                events.append(_event(rng, user_id, ts, "error", {"code": rng.choice(["timeout", "403", "500"])}))
            events.append(_event(rng, user_id, ts, "page_view", {"page": rng.choice(PAGES)}))
    for day in range(31, 61):
        if rng.random() < 0.2:
            ts = created + timedelta(days=day, hours=rng.randint(8, 20))
            events.append(_event(rng, user_id, ts, "login", {}))
            events.append(_event(rng, user_id, ts, "page_view", {"page": "/dashboard"}))
    return events


def _generate_fraud_events(rng, user_id, created):
    events = []
    for day in range(3):
        for _ in range(rng.randint(15, 30)):
            hour = rng.choice([2, 3, 4, 23, 0, 1])
            ts = created + timedelta(days=day, hours=hour, minutes=rng.randint(0, 59))
            event_type = rng.choices(
                ["api_call", "payment", "message_sent", "signup"],
                weights=[0.3, 0.3, 0.3, 0.1], k=1,
            )[0]
            props = {}
            if event_type == "payment":
                props = {"amount": round(rng.uniform(0.50, 4.99), 2), "currency": "USD"}
            elif event_type == "message_sent":
                props = {"template": True, "length": rng.randint(10, 20)}
            elif event_type == "api_call":
                props = {"endpoint": "/api/bulk", "count": rng.randint(50, 500)}
            events.append(_event(rng, user_id, ts, event_type, props))
    return events


def _generate_confused_events(rng, user_id, created):
    events = []
    for day in range(30):
        ts = created + timedelta(days=day, hours=rng.randint(9, 17))
        events.append(_event(rng, user_id, ts, "login", {}))
        for _ in range(rng.randint(2, 5)):
            ts += timedelta(minutes=rng.randint(1, 15))
            events.append(_event(rng, user_id, ts, "page_view", {"page": rng.choice(PAGES)}))
        if rng.random() < 0.4:
            ts += timedelta(minutes=rng.randint(1, 5))
            events.append(_event(rng, user_id, ts, "search", {"query": rng.choice(SEARCH_QUERIES_CONFUSED)}))
        if rng.random() < 0.25:
            ts += timedelta(minutes=rng.randint(5, 30))
            events.append(_event(rng, user_id, ts, "support_ticket", {"message": rng.choice(SUPPORT_MESSAGES_CONFUSED)}))
    return events


def _generate_normal_events(rng, user_id, created):
    events = []
    for day in range(45):
        if rng.random() < 0.7:
            ts = created + timedelta(days=day, hours=rng.randint(9, 17))
            events.append(_event(rng, user_id, ts, "login", {}))
            for _ in range(rng.randint(3, 10)):
                ts += timedelta(minutes=rng.randint(1, 20))
                event_type = rng.choices(
                    ["page_view", "feature_use", "api_call"],
                    weights=[0.5, 0.3, 0.2], k=1,
                )[0]
                props = {}
                if event_type == "page_view":
                    props = {"page": rng.choice(PAGES)}
                elif event_type == "feature_use":
                    props = {"feature": rng.choice(FEATURES)}
                events.append(_event(rng, user_id, ts, event_type, props))
    return events


def _event(rng, user_id, ts, event_type, properties):
    return {
        "event_id": str(uuid.UUID(int=rng.getrandbits(128))),
        "user_id": user_id,
        "timestamp": ts.isoformat(),
        "event_type": event_type,
        "properties": json.dumps(properties),
    }
