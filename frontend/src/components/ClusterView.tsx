import { useState } from "react";
import type { UxCluster } from "../api/types";

interface ClusterViewProps {
  clusters: UxCluster[];
}

export function ClusterView({ clusters }: ClusterViewProps) {
  const [expanded, setExpanded] = useState<string | null>(null);

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {clusters.map((cluster) => (
        <div
          key={cluster.cluster_id}
          className="bg-gray-900 border border-gray-800 rounded-lg p-4 cursor-pointer hover:border-gray-600 transition-colors"
          onClick={() => setExpanded(expanded === cluster.cluster_id ? null : cluster.cluster_id)}
        >
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono text-blue-400 bg-blue-950 px-2 py-0.5 rounded">
              {cluster.feature_area}
            </span>
            <span className="text-xs text-gray-500">{cluster.message_count} reports</span>
          </div>
          <h4 className="font-semibold text-gray-100 mb-2">{cluster.label}</h4>
          <p className="text-sm text-gray-400 mb-3">{cluster.auto_summary}</p>

          {expanded === cluster.cluster_id && (
            <div className="mt-3 pt-3 border-t border-gray-800">
              <h5 className="text-xs font-semibold text-gray-300 uppercase mb-2">Example Messages</h5>
              <ul className="space-y-1.5">
                {cluster.example_messages.map((msg, i) => (
                  <li key={i} className="text-xs text-gray-500 pl-3 border-l-2 border-gray-700">{msg}</li>
                ))}
              </ul>
              <div className="mt-3 p-2 bg-green-950 border border-green-800 rounded text-xs text-green-300">
                <span className="font-semibold">Suggested Fix: </span>
                {cluster.suggested_fix}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
