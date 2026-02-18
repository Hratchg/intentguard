from pydantic import BaseModel


class UserSummary(BaseModel):
    user_id: str
    name: str
    email: str
    created_at: str
    account_type: str
    scenario_tag: str
    churn_score: float | None = None
    fraud_score: float | None = None


class Event(BaseModel):
    event_id: str
    user_id: str
    timestamp: str
    event_type: str
    properties: dict


class RiskScore(BaseModel):
    score_type: str
    score: float
    confidence: float
    top_features: list
    explanation: str
    recommended_action: str
    computed_at: str


class UserDetail(BaseModel):
    user_id: str
    name: str
    email: str
    created_at: str
    account_type: str
    scenario_tag: str
    risk_scores: list[RiskScore]


class UxCluster(BaseModel):
    cluster_id: str
    label: str
    feature_area: str
    message_count: int
    example_messages: list[str]
    auto_summary: str
    suggested_fix: str


class OverviewStats(BaseModel):
    total_users: int
    total_events: int
    high_risk_churn: int
    high_risk_fraud: int
    cluster_count: int


class TimelineResponse(BaseModel):
    events: list[Event]
    total: int
