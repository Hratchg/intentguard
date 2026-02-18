import { motion } from "framer-motion";

const TECH = [
  { name: "FastAPI", category: "Backend" },
  { name: "scikit-learn", category: "ML" },
  { name: "SQLite", category: "Database" },
  { name: "React", category: "Frontend" },
  { name: "TypeScript", category: "Language" },
  { name: "Tailwind CSS", category: "Styling" },
  { name: "Recharts", category: "Visualization" },
  { name: "TanStack Query", category: "Data Fetching" },
  { name: "Framer Motion", category: "Animation" },
  { name: "Docker", category: "Deployment" },
];

export function TechStackSection() {
  return (
    <section className="max-w-4xl mx-auto px-6 py-24">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <h2 className="text-3xl font-bold mb-10">Tech Stack</h2>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {TECH.map((t) => (
            <div key={t.name} className="bg-gray-900 border border-gray-800 rounded-lg p-3 text-center">
              <div className="text-sm font-semibold text-gray-200">{t.name}</div>
              <div className="text-xs text-gray-500">{t.category}</div>
            </div>
          ))}
        </div>
      </motion.div>
    </section>
  );
}
