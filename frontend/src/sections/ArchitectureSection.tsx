import { motion } from "framer-motion";

const STEPS = [
  { label: "Event Ingestion", desc: "Collect events from APIs & logs" },
  { label: "Session Builder", desc: "Group into user journeys" },
  { label: "Feature Extraction", desc: "Compute behavioral signals" },
  { label: "ML Scoring", desc: "Churn, fraud & anomaly models" },
  { label: "Explanation Engine", desc: "Plain English reasoning" },
  { label: "Action Recommender", desc: "Prioritized interventions" },
];

export function ArchitectureSection() {
  return (
    <section className="max-w-5xl mx-auto px-6 py-24">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <h2 className="text-3xl font-bold mb-2">How It Works</h2>
        <p className="text-gray-500 mb-10">A simple 6-step pipeline from raw events to actionable intelligence.</p>
      </motion.div>
      <div className="flex flex-wrap items-center justify-center gap-2">
        {STEPS.map((step, i) => (
          <motion.div
            key={step.label}
            initial={{ opacity: 0, scale: 0.8 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.4, delay: i * 0.1 }}
            className="flex items-center gap-2"
          >
            <div className="bg-gray-900 border border-gray-800 rounded-lg p-4 text-center w-40">
              <div className="text-xs text-blue-400 font-mono mb-1">Step {i + 1}</div>
              <div className="text-sm font-semibold text-gray-100">{step.label}</div>
              <div className="text-xs text-gray-500 mt-1">{step.desc}</div>
            </div>
            {i < STEPS.length - 1 && (
              <div className="text-gray-600 text-lg">&rarr;</div>
            )}
          </motion.div>
        ))}
      </div>
    </section>
  );
}
