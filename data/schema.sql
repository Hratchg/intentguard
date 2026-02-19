CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    created_at TEXT NOT NULL,
    account_type TEXT NOT NULL CHECK(account_type IN ('free', 'pro', 'enterprise')),
    scenario_tag TEXT NOT NULL CHECK(scenario_tag IN ('churn', 'fraud', 'normal', 'confused'))
);

CREATE TABLE IF NOT EXISTS events (
    event_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(user_id),
    timestamp TEXT NOT NULL,
    event_type TEXT NOT NULL,
    properties TEXT NOT NULL DEFAULT '{}',
    CHECK(event_type IN (
        'page_view', 'api_call', 'login', 'payment', 'support_ticket',
        'search', 'feature_use', 'error', 'signup', 'message_sent'
    ))
);

CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);

CREATE TABLE IF NOT EXISTS risk_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL REFERENCES users(user_id),
    score_type TEXT NOT NULL CHECK(score_type IN ('churn', 'fraud', 'abuse')),
    score REAL NOT NULL CHECK(score >= 0 AND score <= 100),
    confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 1),
    top_features TEXT NOT NULL DEFAULT '[]',
    explanation TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    computed_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_risk_user ON risk_scores(user_id);

CREATE TABLE IF NOT EXISTS ux_clusters (
    cluster_id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    feature_area TEXT NOT NULL,
    message_count INTEGER NOT NULL,
    example_messages TEXT NOT NULL DEFAULT '[]',
    auto_summary TEXT NOT NULL,
    suggested_fix TEXT NOT NULL
);
