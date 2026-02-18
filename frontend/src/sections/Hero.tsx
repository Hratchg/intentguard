import { motion } from "framer-motion";
import type { OverviewStats } from "../api/types";

interface HeroProps {
  stats?: OverviewStats;
  onTryDemo: () => void;
}

export function Hero({ stats, onTryDemo }: HeroProps) {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950" />
      <div className="relative z-10 text-center px-6 max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-6xl font-extrabold tracking-tight mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-400">
              IntentGuard
            </span>
          </h1>
          <p className="text-xl text-gray-400 mb-2">
            Explainable User-Behavior & Risk Intelligence
          </p>
          <p className="text-gray-500 mb-8 max-w-2xl mx-auto">
            Detect churn risk, fraud patterns, and UX confusion in real time.
            Understand <em>why</em> users behave the way they do — and what to do about it.
          </p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="flex items-center justify-center gap-4 mb-12"
        >
          <button
            onClick={onTryDemo}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg transition-colors"
          >
            Try Demo
          </button>
          <a
            href="https://github.com"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-gray-200 font-semibold rounded-lg transition-colors"
          >
            GitHub
          </a>
        </motion.div>

        {stats && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="grid grid-cols-4 gap-6 max-w-lg mx-auto"
          >
            {[
              { label: "Users Tracked", value: stats.total_users },
              { label: "Events Analyzed", value: stats.total_events.toLocaleString() },
              { label: "Churn Alerts", value: stats.high_risk_churn },
              { label: "UX Clusters", value: stats.cluster_count },
            ].map((stat) => (
              <div key={stat.label}>
                <div className="text-2xl font-bold text-gray-100">{stat.value}</div>
                <div className="text-xs text-gray-500 uppercase tracking-wider">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        )}
      </div>
    </section>
  );
}
