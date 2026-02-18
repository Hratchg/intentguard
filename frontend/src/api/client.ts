import type {
  UserSummary, UserDetail, TimelineResponse,
  RiskScore, UxCluster, OverviewStats,
} from "./types";

const BASE = "/api";

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export const api = {
  getUsers: (params?: { scenario?: string; risk_level?: string }) => {
    const qs = new URLSearchParams(params as Record<string, string>).toString();
    return fetchJson<UserSummary[]>(`/users${qs ? `?${qs}` : ""}`);
  },
  getUser: (id: string) => fetchJson<UserDetail>(`/users/${id}`),
  getTimeline: (id: string, params?: { event_type?: string; limit?: number; offset?: number }) => {
    const qs = new URLSearchParams(
      Object.fromEntries(Object.entries(params || {}).map(([k, v]) => [k, String(v)]))
    ).toString();
    return fetchJson<TimelineResponse>(`/users/${id}/timeline${qs ? `?${qs}` : ""}`);
  },
  getRisk: (id: string) => fetchJson<RiskScore[]>(`/users/${id}/risk`),
  recalculateRisk: (id: string) =>
    fetchJson<RiskScore[]>(`/users/${id}/risk/recalculate`),
  getClusters: () => fetchJson<UxCluster[]>("/insights/clusters"),
  getCluster: (id: string) => fetchJson<UxCluster>(`/insights/clusters/${id}`),
  getStats: () => fetchJson<OverviewStats>("/stats/overview"),
};
