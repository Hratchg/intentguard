FEATURE_TEMPLATES = {
    "pricing_page_views": "Visited the pricing page {value:.0f} times",
    "error_rate": "Encountered errors in {pct} of interactions",
    "error_count": "Hit {value:.0f} errors total",
    "activity_trend": "Activity trend score: {value:+.2f}",
    "login_count": "Logged in {value:.0f} times",
    "unusual_hour_ratio": "{pct} of activity during unusual hours",
    "payment_count": "Made {value:.0f} payments",
    "small_payment_ratio": "{pct} of payments were under $5",
    "template_message_ratio": "{pct} of messages used templates",
    "bulk_api_ratio": "{pct} of API calls were bulk operations",
    "support_ticket_count": "Filed {value:.0f} support tickets",
    "search_count": "Searched {value:.0f} times",
    "events_per_day": "Average {value:.1f} events per day",
    "span_days": "Active over {value:.0f} days",
    "feature_use_count": "Used {value:.0f} features",
}

ACTION_THRESHOLDS = {
    "churn": [
        (80, "Urgent: Schedule a personal check-in call within 24 hours"),
        (60, "Send targeted re-engagement email with feature highlights"),
        (40, "Add to watch list for weekly review"),
        (0, "No action needed - healthy engagement"),
    ],
    "fraud": [
        (80, "Block account and escalate to Trust & Safety for review"),
        (60, "Rate-limit API access and require identity verification"),
        (40, "Flag for manual review within 48 hours"),
        (0, "No action needed - normal patterns"),
    ],
}


def explain_features(top_features: list[tuple[str, float]]) -> str:
    parts = []
    for name, value in top_features[:5]:
        template = FEATURE_TEMPLATES.get(name)
        if template:
            pct = f"{abs(value) * 100:.0f}%" if abs(value) <= 1 else f"{value:.1f}"
            text = template.format(value=value, pct=pct)
        else:
            text = f"{name.replace('_', ' ').title()}: {value:.2f}"
        parts.append(f"- {text}")
    return "\n".join(parts)


def recommend_action(score_type: str, score: float) -> str:
    thresholds = ACTION_THRESHOLDS.get(score_type, ACTION_THRESHOLDS["churn"])
    for threshold, action in thresholds:
        if score >= threshold:
            return action
    return "Monitor"
