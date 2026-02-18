import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";

interface FeatureImportanceChartProps {
  features: [string, number][];
}

export function FeatureImportanceChart({ features }: FeatureImportanceChartProps) {
  const data = features.map(([name, value]) => ({
    name: name.replace(/_/g, " "),
    value: Math.abs(Number(value)),
    raw: Number(value),
  }));

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-lg p-4">
      <h3 className="text-sm font-semibold text-gray-200 uppercase tracking-wider mb-3">
        Top Contributing Factors
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} layout="vertical" margin={{ left: 100 }}>
          <XAxis type="number" stroke="#4b5563" tick={{ fill: "#9ca3af", fontSize: 11 }} />
          <YAxis
            type="category" dataKey="name"
            stroke="#4b5563" tick={{ fill: "#d1d5db", fontSize: 11 }} width={100}
          />
          <Tooltip
            contentStyle={{ backgroundColor: "#1f2937", border: "1px solid #374151", borderRadius: 8 }}
            labelStyle={{ color: "#f3f4f6" }}
            itemStyle={{ color: "#93c5fd" }}
          />
          <Bar dataKey="value" radius={[0, 4, 4, 0]}>
            {data.map((_, i) => (
              <Cell key={i} fill={i === 0 ? "#3b82f6" : i === 1 ? "#60a5fa" : "#93c5fd"} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
