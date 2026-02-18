import { motion } from "framer-motion";

interface ScenariosSectionProps {
  onExplore: (scenario?: string) => void;
}

const SCENARIOS = [
  {
    tag: "churn",
    title: "Churn Early Warning",
    input: "Onboarding failures, pricing page views, declining activity",
    output: "Churn risk score + trend, reason in plain English, recommended intervention",
    color: "from-red-600 to-orange-600",
  },
  {
    tag: "fraud",
    title: "Fraud Pattern Detection",
    input: "Rapid account creation, repeated small payments, template messages",
    output: "Fraud risk score, evidence list ranked by importance, suggested action",
    color: "from-purple-600 to-pink-600",
  },
  {
    tag: "confused",
    title: "UX Confusion Detector",
    input: "Support tickets, search queries, repeated navigation patterns",
    output: "Confusion cluster summary, example messages, suggested product fix",
    color: "from-blue-600 to-cyan-600",
  },
];

export function ScenariosSection({ onExplore }: ScenariosSectionProps) {
  return (
    <section className="max-w-6xl mx-auto px-6 py-24">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <h2 className="text-3xl font-bold mb-2">Proof It Works</h2>
        <p className="text-gray-500 mb-10">Three real-world scenarios with inputs and outputs.</p>
      </motion.div>
      <div className="grid md:grid-cols-3 gap-6">
        {SCENARIOS.map((s, i) => (
          <motion.div
            key={s.tag}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: i * 0.15 }}
            className="bg-gray-900 border border-gray-800 rounded-xl p-6 flex flex-col"
          >
            <div className={`h-1 w-16 rounded bg-gradient-to-r ${s.color} mb-4`} />
            <h3 className="text-lg font-semibold text-gray-100 mb-3">{s.title}</h3>
            <div className="mb-3">
              <span className="text-xs text-gray-500 uppercase tracking-wider">Input</span>
              <p className="text-sm text-gray-400 mt-1">{s.input}</p>
            </div>
            <div className="mb-6 flex-1">
              <span className="text-xs text-gray-500 uppercase tracking-wider">Output</span>
              <p className="text-sm text-gray-400 mt-1">{s.output}</p>
            </div>
            <button
              onClick={() => onExplore(s.tag)}
              className="w-full py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm font-medium rounded-lg transition-colors"
            >
              Explore in Dashboard
            </button>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
