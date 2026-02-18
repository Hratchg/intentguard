interface ActionCardProps {
  action: string;
  score: number;
}

const SEVERITY_CONFIG = [
  { min: 80, label: "CRITICAL", bg: "bg-red-950", border: "border-red-700", text: "text-red-400" },
  { min: 60, label: "HIGH", bg: "bg-orange-950", border: "border-orange-700", text: "text-orange-400" },
  { min: 40, label: "MEDIUM", bg: "bg-yellow-950", border: "border-yellow-700", text: "text-yellow-400" },
  { min: 0, label: "LOW", bg: "bg-green-950", border: "border-green-700", text: "text-green-400" },
];

export function ActionCard({ action, score }: ActionCardProps) {
  const severity = SEVERITY_CONFIG.find((s) => score >= s.min)!;
  return (
    <div className={`${severity.bg} border ${severity.border} rounded-lg p-4`}>
      <div className="flex items-center gap-2 mb-2">
        <span className={`text-xs font-bold ${severity.text} uppercase`}>{severity.label}</span>
        <span className="text-xs text-gray-500">Recommended Action</span>
      </div>
      <p className="text-sm text-gray-200">{action}</p>
    </div>
  );
}
