import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import { RiskGauge } from "../components/RiskGauge";
import { TimelineView } from "../components/TimelineView";
import { ExplanationPanel } from "../components/ExplanationPanel";
import { ActionCard } from "../components/ActionCard";
import { FeatureImportanceChart } from "../components/FeatureImportanceChart";

interface UserPanelProps {
  userId: string;
}

export function UserPanel({ userId }: UserPanelProps) {
  const { data: user } = useQuery({
    queryKey: ["user", userId],
    queryFn: () => api.getUser(userId),
  });

  const { data: timeline } = useQuery({
    queryKey: ["timeline", userId],
    queryFn: () => api.getTimeline(userId, { limit: 200 }),
  });

  if (!user) return <div className="flex-1 flex items-center justify-center text-gray-600">Loading...</div>;

  const churnRisk = user.risk_scores.find((r) => r.score_type === "churn");
  const fraudRisk = user.risk_scores.find((r) => r.score_type === "fraud");
  const primaryRisk = (churnRisk?.score || 0) >= (fraudRisk?.score || 0) ? churnRisk : fraudRisk;

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-100">{user.name}</h2>
          <p className="text-sm text-gray-500">
            {user.email} &middot; {user.account_type} &middot; Joined{" "}
            {new Date(user.created_at).toLocaleDateString()}
          </p>
        </div>
        <span className="text-xs font-mono bg-gray-800 text-gray-400 px-2 py-1 rounded">
          {user.scenario_tag}
        </span>
      </div>

      <div className="flex gap-8">
        {churnRisk && <RiskGauge label="Churn Risk" score={churnRisk.score} />}
        {fraudRisk && <RiskGauge label="Fraud Risk" score={fraudRisk.score} />}
      </div>

      {timeline && (
        <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-gray-200 uppercase tracking-wider mb-2">
            Event Timeline ({timeline.total} events)
          </h3>
          <TimelineView events={timeline.events} />
        </div>
      )}

      {primaryRisk && (
        <div className="grid md:grid-cols-2 gap-4">
          <ExplanationPanel risk={primaryRisk} />
          <div className="space-y-4">
            <ActionCard action={primaryRisk.recommended_action} score={primaryRisk.score} />
            <FeatureImportanceChart features={primaryRisk.top_features} />
          </div>
        </div>
      )}
    </div>
  );
}
