import json
from datetime import datetime
from collections import Counter


def extract_user_features(events: list[dict]) -> dict:
    if not events:
        return _empty_features()

    timestamps = [datetime.fromisoformat(e["timestamp"]) for e in events]
    types = [e["event_type"] for e in events]
    type_counts = Counter(types)

    total = len(events)
    span_days = max((max(timestamps) - min(timestamps)).days, 1)

    props = []
    for e in events:
        p = e.get("properties", "{}")
        props.append(json.loads(p) if isinstance(p, str) else p)

    page_views = [p.get("page", "") for e, p in zip(events, props) if e["event_type"] == "page_view"]
    pricing_views = sum(1 for p in page_views if p == "/pricing")

    hours = [t.hour for t in timestamps]
    unusual_hour_ratio = sum(1 for h in hours if h < 6 or h > 22) / max(len(hours), 1)

    payments = [p for e, p in zip(events, props) if e["event_type"] == "payment"]
    payment_count = len(payments)
    avg_payment = sum(p.get("amount", 0) for p in payments) / max(payment_count, 1)
    small_payment_ratio = sum(1 for p in payments if p.get("amount", 0) < 5) / max(payment_count, 1)

    support_count = type_counts.get("support_ticket", 0)
    search_count = type_counts.get("search", 0)

    mid = timestamps[0] + (timestamps[-1] - timestamps[0]) / 2
    first_half = sum(1 for t in timestamps if t <= mid)
    second_half = total - first_half
    activity_trend = (second_half - first_half) / max(total, 1)

    messages = [p for e, p in zip(events, props) if e["event_type"] == "message_sent"]
    template_ratio = sum(1 for m in messages if m.get("template")) / max(len(messages), 1)

    api_calls = [p for e, p in zip(events, props) if e["event_type"] == "api_call"]
    bulk_api_ratio = sum(1 for a in api_calls if a.get("count", 0) > 100) / max(len(api_calls), 1)

    return {
        "total_events": total,
        "span_days": span_days,
        "events_per_day": total / span_days,
        "login_count": type_counts.get("login", 0),
        "error_count": type_counts.get("error", 0),
        "error_rate": type_counts.get("error", 0) / total,
        "page_view_count": type_counts.get("page_view", 0),
        "pricing_page_views": pricing_views,
        "feature_use_count": type_counts.get("feature_use", 0),
        "payment_count": payment_count,
        "avg_payment_amount": avg_payment,
        "small_payment_ratio": small_payment_ratio,
        "support_ticket_count": support_count,
        "search_count": search_count,
        "unusual_hour_ratio": unusual_hour_ratio,
        "activity_trend": activity_trend,
        "template_message_ratio": template_ratio,
        "bulk_api_ratio": bulk_api_ratio,
        "unique_event_types": len(type_counts),
    }


def _empty_features():
    return {k: 0 for k in [
        "total_events", "span_days", "events_per_day", "login_count",
        "error_count", "error_rate", "page_view_count", "pricing_page_views",
        "feature_use_count", "payment_count", "avg_payment_amount",
        "small_payment_ratio", "support_ticket_count", "search_count",
        "unusual_hour_ratio", "activity_trend", "template_message_ratio",
        "bulk_api_ratio", "unique_event_types",
    ]}


FEATURE_NAMES = list(_empty_features().keys())
