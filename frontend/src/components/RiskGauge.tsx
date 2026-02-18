interface RiskGaugeProps {
  label: string;
  score: number;
  size?: number;
}

export function RiskGauge({ label, score, size = 120 }: RiskGaugeProps) {
  const radius = (size - 16) / 2;
  const circumference = 2 * Math.PI * radius;
  const progress = (score / 100) * circumference;
  const color =
    score >= 70 ? "#ef4444" : score >= 40 ? "#f59e0b" : "#22c55e";

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#1f2937" strokeWidth={8} />
        <circle
          cx={size / 2} cy={size / 2} r={radius} fill="none"
          stroke={color} strokeWidth={8}
          strokeDasharray={circumference}
          strokeDashoffset={circumference - progress}
          strokeLinecap="round"
          className="transition-all duration-700"
        />
        <text
          x={size / 2} y={size / 2}
          textAnchor="middle" dominantBaseline="central"
          className="rotate-90 origin-center fill-gray-100 text-xl font-bold"
          style={{ fontSize: size * 0.22 }}
        >
          {Math.round(score)}
        </text>
      </svg>
      <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">{label}</span>
    </div>
  );
}
