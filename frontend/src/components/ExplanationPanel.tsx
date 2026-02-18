import type { RiskScore } from "../api/types";

interface ExplanationPanelProps {
  risk: RiskScore;
}

export function ExplanationPanel({ risk }: ExplanationPanelProps) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-gray-200 uppercase tracking-wider">Why this score?</h3>
        <span className="text-xs text-gray-500">Confidence: {(risk.confidence * 100).toFixed(0)}%</span>
      </div>
      <div className="space-y-2">
        {risk.top_features.map(([feature, value], i) => (
          <div key={feature} className="flex items-center gap-3">
            <span className="text-xs text-gray-500 w-4">{i + 1}.</span>
            <div className="flex-1">
              <div className="text-sm text-gray-300">{feature.replace(/_/g, " ")}</div>
              <div className="h-1.5 bg-gray-800 rounded-full mt-1">
                <div
                  className="h-full bg-blue-500 rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(Math.abs(Number(value)) * 10, 100)}%` }}
                />
              </div>
            </div>
            <span className="text-xs font-mono text-gray-400">
              {typeof value === "number" ? value.toFixed(2) : value}
            </span>
          </div>
        ))}
      </div>
      <pre className="mt-4 text-xs text-gray-500 whitespace-pre-wrap">{risk.explanation}</pre>
    </div>
  );
}
