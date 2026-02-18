import { motion } from "framer-motion";

export function WhySection() {
  return (
    <section className="max-w-4xl mx-auto px-6 py-24">
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.6 }}
      >
        <h2 className="text-3xl font-bold mb-6">Why This Exists</h2>
        <p className="text-gray-400 text-lg mb-8">
          Traditional analytics tell you <strong className="text-gray-200">what</strong> happened.
          IntentGuard tells you <strong className="text-gray-200">why</strong> — and what to do next.
          Instead of reactive firefighting, your product, ops, and trust & safety teams get
          proactive, explainable intelligence.
        </p>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { title: "Product Teams", desc: "Discover UX confusion patterns before they become churn." },
            { title: "Operations", desc: "Prioritize interventions with AI-ranked risk scores." },
            { title: "Trust & Safety", desc: "Detect fraud and abuse patterns with evidence trails." },
          ].map((item) => (
            <div key={item.title} className="bg-gray-900 border border-gray-800 rounded-lg p-5">
              <h3 className="font-semibold text-gray-100 mb-2">{item.title}</h3>
              <p className="text-sm text-gray-500">{item.desc}</p>
            </div>
          ))}
        </div>
      </motion.div>
    </section>
  );
}
