import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "../api/client";
import type { UserSummary } from "../api/types";

interface UserSidebarProps {
  selectedId: string | null;
  onSelect: (id: string) => void;
  initialScenario?: string;
}

export function UserSidebar({ selectedId, onSelect, initialScenario }: UserSidebarProps) {
  const [search, setSearch] = useState("");
  const [scenario, setScenario] = useState(initialScenario || "");

  const { data: users = [] } = useQuery({
    queryKey: ["users", scenario],
    queryFn: () => api.getUsers(scenario ? { scenario } : undefined),
  });

  const filtered = users.filter(
    (u) =>
      u.name.toLowerCase().includes(search.toLowerCase()) ||
      u.email.toLowerCase().includes(search.toLowerCase())
  );

  const riskBadge = (u: UserSummary) => {
    const maxScore = Math.max(u.churn_score || 0, u.fraud_score || 0);
    if (maxScore >= 70) return "bg-red-500";
    if (maxScore >= 40) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="w-72 border-r border-gray-800 flex flex-col h-full bg-gray-950">
      <div className="p-3 border-b border-gray-800 space-y-2">
        <input
          type="text"
          placeholder="Search users..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-gray-900 border border-gray-700 rounded px-3 py-1.5 text-sm text-gray-200 placeholder-gray-600 focus:outline-none focus:border-blue-500"
        />
        <select
          value={scenario}
          onChange={(e) => setScenario(e.target.value)}
          className="w-full bg-gray-900 border border-gray-700 rounded px-3 py-1.5 text-sm text-gray-200"
        >
          <option value="">All Scenarios</option>
          <option value="churn">Churn</option>
          <option value="fraud">Fraud</option>
          <option value="confused">Confused</option>
          <option value="normal">Normal</option>
        </select>
      </div>
      <div className="flex-1 overflow-y-auto">
        {filtered.map((user) => (
          <button
            key={user.user_id}
            onClick={() => onSelect(user.user_id)}
            className={`w-full text-left px-3 py-2.5 border-b border-gray-800/50 hover:bg-gray-900 transition-colors ${
              selectedId === user.user_id ? "bg-gray-900 border-l-2 border-l-blue-500" : ""
            }`}
          >
            <div className="flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${riskBadge(user)}`} />
              <span className="text-sm font-medium text-gray-200 truncate">{user.name}</span>
            </div>
            <div className="text-xs text-gray-500 mt-0.5 ml-4">{user.email}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
