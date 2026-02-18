export interface UserSummary {
  user_id: string;
  name: string;
  email: string;
  created_at: string;
  account_type: string;
  scenario_tag: string;
  churn_score: number | null;
  fraud_score: number | null;
}

export interface Event {
  event_id: string;
  user_id: string;
  timestamp: string;
  event_type: string;
  properties: Record<string, unknown>;
}

export interface RiskScore {
  score_type: string;
  score: number;
  confidence: number;
  top_features: [string, number][];
  explanation: string;
  recommended_action: string;
  computed_at: string;
}

export interface UserDetail extends UserSummary {
  risk_scores: RiskScore[];
}

export interface UxCluster {
  cluster_id: string;
  label: string;
  feature_area: string;
  message_count: number;
  example_messages: string[];
  auto_summary: string;
  suggested_fix: string;
}

export interface OverviewStats {
  total_users: number;
  total_events: number;
  high_risk_churn: number;
  high_risk_fraud: number;
  cluster_count: number;
}

export interface TimelineResponse {
  events: Event[];
  total: number;
}
